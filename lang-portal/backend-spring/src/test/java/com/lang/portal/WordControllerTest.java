package com.lang.portal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import com.lang.portal.controller.WordController;
import com.lang.portal.dto.WordCountDTO;
import com.lang.portal.dto.WordDTO;
import com.lang.portal.entities.Word;
import com.lang.portal.service.WordService;

import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
public class WordControllerTest {

    @Mock
    private WordService wordService;

    @InjectMocks
    private WordController wordController;

    @Test
    void testGetAllWords() {
        Word word1 = new Word();
        word1.setId(1L);
        word1.setEnglish("Hello");
        word1.setSpanish("Hola");
        word1.setPronunciation("həˈloʊ");

        Word word2 = new Word();
        word2.setId(2L);
        word2.setEnglish("Goodbye");
        word2.setSpanish("Adiós");
        word2.setPronunciation("ɡʊdˈbaɪ");

        List<Word> wordList = List.of(word1, word2);
        Page<Word> wordPage = new PageImpl<>(wordList, PageRequest.of(0, 10), wordList.size());

        when(wordService.getAllWords(1, "english", "asc")).thenReturn(wordPage);

        ResponseEntity<Page<WordDTO>> response = wordController.getAllWords(1, "english", "asc");

        assertNotNull(response);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(2, response.getBody().getContent().size());

        verify(wordService, times(1)).getAllWords(1, "english", "asc");
    }

    @Test
    void testGetWordCounts() {
        WordCountDTO wordCountDTO = new WordCountDTO();
        wordCountDTO.setTotalWords(100);

        when(wordService.getWordCounts()).thenReturn(wordCountDTO);

        ResponseEntity<WordCountDTO> response = wordController.getWordCounts();

        assertNotNull(response);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(100, response.getBody().getTotalWords());

        verify(wordService, times(1)).getWordCounts();
    }

}
