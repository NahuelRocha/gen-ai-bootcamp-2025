package com.lang.portal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;

import com.lang.portal.dto.WordCountDTO;
import com.lang.portal.entities.Word;
import com.lang.portal.exceptions.ResourceNotFoundException;
import com.lang.portal.repository.WordRepository;
import com.lang.portal.service.WordService;

@ExtendWith(MockitoExtension.class)
public class WordServiceTest {

    @Mock
    private WordRepository wordRepository;

    @InjectMocks
    private WordService wordService;

    @Test
    void testGetAllWords() {
        // Given
        int page = 1;
        String sortBy = "english";
        String order = "asc";
        Page<Word> expectedPage = new PageImpl<>(List.of(new Word(), new Word())); // Mocked data

        when(wordRepository.findAll(any(Pageable.class))).thenReturn(expectedPage);

        // When
        Page<Word> actualPage = wordService.getAllWords(page, sortBy, order);

        // Then
        assertEquals(expectedPage, actualPage);
        verify(wordRepository).findAll(any(Pageable.class));
    }

    // GETWORDBYID TEST

    @Test
    void testGetWordById_Success() {
        // Given
        Long wordId = 1L;
        Word expectedWord = new Word();
        when(wordRepository.findById(wordId)).thenReturn(Optional.of(expectedWord));

        // When
        Word actualWord = wordService.getWordById(wordId);

        // Then
        assertEquals(expectedWord, actualWord);
        verify(wordRepository).findById(wordId);
    }

    @Test
    void testGetWordById_NotFound() {
        // Given
        Long wordId = 1L;
        when(wordRepository.findById(wordId)).thenReturn(Optional.empty());

        // When & Then
        assertThrows(ResourceNotFoundException.class, () -> wordService.getWordById(wordId));
    }

    // updateWordStats test

    @Test
    void testUpdateWordStats_Correct() {
        // Given
        Long wordId = 1L;
        Word word = new Word();
        word.setCorrectCount(0);
        when(wordRepository.findById(wordId)).thenReturn(Optional.of(word));

        // When
        wordService.updateWordStats(wordId, true);

        // Then
        assertEquals(1, word.getCorrectCount());
        verify(wordRepository).save(word);
    }

    @Test
    void testUpdateWordStats_Incorrect() {
        // Given
        Long wordId = 1L;
        Word word = new Word();
        word.setWrongCount(0);
        when(wordRepository.findById(wordId)).thenReturn(Optional.of(word));

        // When
        wordService.updateWordStats(wordId, false);

        // Then
        assertEquals(1, word.getWrongCount());
        verify(wordRepository).save(word);
    }

    // getWordCounts test

    @Test
    void testGetWordCounts() {
        // Given
        when(wordRepository.countTotalWords()).thenReturn(100L);
        when(wordRepository.countWordsLearned()).thenReturn(50L);

        // When
        WordCountDTO result = wordService.getWordCounts();

        // Then
        assertEquals(100L, result.getTotalWords());
        assertEquals(50L, result.getTotalWordsLearned());
    }

}
