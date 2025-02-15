package com.lang.portal.controller;

import org.springframework.beans.BeanUtils;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.lang.portal.dto.WordCountDTO;
import com.lang.portal.dto.WordDTO;
import com.lang.portal.entities.Word;
import com.lang.portal.service.WordService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/words")
@RequiredArgsConstructor
public class WordController {
    private final WordService wordService;

    @GetMapping
    public ResponseEntity<Page<WordDTO>> getAllWords(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "english") String sortBy,
            @RequestParam(defaultValue = "asc") String order) {

        Page<Word> words = wordService.getAllWords(page, sortBy, order);
        Page<WordDTO> wordDTOs = words.map(word -> {
            WordDTO dto = new WordDTO();
            BeanUtils.copyProperties(word, dto);
            return dto;
        });

        return ResponseEntity.ok(wordDTOs);
    }

    @GetMapping("/count")
    public ResponseEntity<WordCountDTO> getWordCounts() {
        WordCountDTO dto = wordService.getWordCounts();
        return ResponseEntity.ok(dto);
    }
}
