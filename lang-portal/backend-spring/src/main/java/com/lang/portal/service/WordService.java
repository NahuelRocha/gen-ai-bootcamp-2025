package com.lang.portal.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.lang.portal.dto.WordCountDTO;
import com.lang.portal.entities.Word;
import com.lang.portal.exceptions.ResourceNotFoundException;
import com.lang.portal.repository.WordRepository;

import lombok.RequiredArgsConstructor;

@Service
@Transactional
@RequiredArgsConstructor
public class WordService {
    private final WordRepository wordRepository;

    public Page<Word> getAllWords(int page, String sortBy, String order) {
        Sort.Direction direction = Sort.Direction.fromString(order.toUpperCase());
        Pageable pageable = PageRequest.of(page - 1, 10, Sort.by(direction, sortBy));
        return wordRepository.findAll(pageable);
    }

    public Word getWordById(Long id) {
        return wordRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Word not found with id: " + id));
    }

    public void updateWordStats(Long wordId, boolean correct) {
        Word word = getWordById(wordId);
        if (correct) {
            word.setCorrectCount(word.getCorrectCount() + 1);
        } else {
            word.setWrongCount(word.getWrongCount() + 1);
        }
        wordRepository.save(word);
    }

    public WordCountDTO getWordCounts() {
        WordCountDTO dto = new WordCountDTO();
        dto.setTotalWords(wordRepository.countTotalWords());
        dto.setTotalWordsLearned(wordRepository.countWordsLearned());
        return dto;
    }
}
