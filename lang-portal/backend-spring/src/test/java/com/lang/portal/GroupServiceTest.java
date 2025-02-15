package com.lang.portal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
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

import com.lang.portal.entities.Group;
import com.lang.portal.entities.Word;
import com.lang.portal.exceptions.ResourceNotFoundException;
import com.lang.portal.repository.GroupRepository;
import com.lang.portal.service.GroupService;

@ExtendWith(MockitoExtension.class)
class GroupServiceTest {

    @Mock
    private GroupRepository groupRepository;

    @InjectMocks
    private GroupService groupService;

    // getGroupWords test

    @Test
    void testGetGroupWords() {
        // Given
        Long groupId = 1L;
        int page = 1;
        Page<Word> expectedPage = new PageImpl<>(List.of(new Word(), new Word())); // Mocked data
        String sortBy = "name";
        String order = "asc";

        when(groupRepository.findWordsByGroupId(eq(groupId), any(Pageable.class))).thenReturn(expectedPage);

        // When
        Page<Word> actualPage = groupService.getGroupWords(groupId, page, sortBy, order);

        // Then
        assertEquals(expectedPage, actualPage);
        verify(groupRepository).findWordsByGroupId(eq(groupId), any(Pageable.class));
    }

    // getGroupById test
    @Test
    void testGetGroupById_Success() {
        // Given
        Long groupId = 1L;
        Group expectedGroup = new Group();
        when(groupRepository.findById(groupId)).thenReturn(Optional.of(expectedGroup));

        // When
        Group actualGroup = groupService.getGroupById(groupId);

        // Then
        assertEquals(expectedGroup, actualGroup);
        verify(groupRepository).findById(groupId);
    }

    @Test
    void testGetGroupById_NotFound() {
        // Given
        Long groupId = 1L;
        when(groupRepository.findById(groupId)).thenReturn(Optional.empty());

        // When & Then
        assertThrows(ResourceNotFoundException.class, () -> groupService.getGroupById(groupId));
    }

    // getAllGroups test

    @Test
    void testGetAllGroups() {
        // Given
        int page = 1;
        Page<Group> expectedPage = new PageImpl<>(List.of(new Group(), new Group())); // Mocked data

        when(groupRepository.findAll(any(Pageable.class))).thenReturn(expectedPage);

        // When
        Page<Group> actualPage = groupService.getAllGroups(page);

        // Then
        assertEquals(expectedPage, actualPage);
        verify(groupRepository).findAll(any(Pageable.class));
    }
}
