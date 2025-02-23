package com.lang.portal;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import com.lang.portal.controller.GroupController;
import com.lang.portal.dto.GroupDTO;
import com.lang.portal.dto.WordDTO;
import com.lang.portal.entities.Group;
import com.lang.portal.entities.Word;
import com.lang.portal.service.GroupService;

import java.util.List;

@ExtendWith(MockitoExtension.class)
class GroupControllerTest {

    @Mock
    private GroupService groupService;

    @InjectMocks
    private GroupController groupController;

    private Page<Group> groupPage;

    @BeforeEach
    void setUp() {
        Group group1 = new Group();
        group1.setId(1L);
        group1.setName("Group 1");

        Group group2 = new Group();
        group2.setId(2L);
        group2.setName("Group 2");

        List<Group> groupList = List.of(group1, group2);
        groupPage = new PageImpl<>(groupList, PageRequest.of(0, 10), groupList.size());
    }

    @Test
    void testGetAllGroups() {
        when(groupService.getAllGroups(1)).thenReturn(groupPage);

        ResponseEntity<Page<GroupDTO>> response = groupController.getAllGroups(1);

        assertNotNull(response);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(2, response.getBody().getContent().size());

        verify(groupService, times(1)).getAllGroups(1);
    }

    @Test
    void testGetGroupWords() {
        Long groupId = 1L;
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

        when(groupService.getGroupWords(groupId, 1, "english", "asc")).thenReturn(wordPage);

        ResponseEntity<Page<WordDTO>> response = groupController.getGroupWords(groupId, 1, "english", "asc");

        assertNotNull(response);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(2, response.getBody().getContent().size());

        verify(groupService, times(1)).getGroupWords(groupId, 1, "english", "asc");
    }
}
