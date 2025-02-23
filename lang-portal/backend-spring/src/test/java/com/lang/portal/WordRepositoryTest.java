package com.lang.portal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Optional;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import com.lang.portal.entities.Word;
import com.lang.portal.repository.WordRepository;

@SpringBootTest
@Transactional
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class WordRepositoryTest {

    @Autowired
    private WordRepository wordRepository;

    @Test
    void testInsertAndFindWord() {
        Word word = new Word();
        word.setEnglish("Dog");
        word.setSpanish("Perro");
        word.setPronunciation("dɒɡ");
        wordRepository.save(word);

        Optional<Word> foundWord = wordRepository.findById(word.getId());
        assertTrue(foundWord.isPresent());
        assertEquals("Perro", foundWord.get().getSpanish());
        System.out.println("✅ Palabra insertada y recuperada correctamente");
    }
}
