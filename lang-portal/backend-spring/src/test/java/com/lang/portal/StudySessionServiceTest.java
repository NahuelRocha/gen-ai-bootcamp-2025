package com.lang.portal;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import com.lang.portal.dto.LastStudySessionResponseDTO;
import com.lang.portal.dto.StudySessionRequestDTO;
import com.lang.portal.dto.StudySessionResponseDTO;
import com.lang.portal.dto.WordReviewRequestDTO;
import com.lang.portal.dto.WordReviewResponseDTO;
import com.lang.portal.entities.Group;
import com.lang.portal.entities.StudyActivity;
import com.lang.portal.entities.StudySession;
import com.lang.portal.entities.Word;
import com.lang.portal.entities.WordReviewItem;
import com.lang.portal.repository.StudyActivityRepository;
import com.lang.portal.repository.StudySessionRepository;
import com.lang.portal.repository.WordReviewItemRepository;
import com.lang.portal.service.GroupService;
import com.lang.portal.service.StudySessionService;
import com.lang.portal.service.WordService;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class StudySessionServiceTest {

    @Mock
    private StudySessionRepository studySessionRepository;

    @Mock
    private GroupService groupService;

    @Mock
    private StudyActivityRepository studyActivityRepository;

    @Mock
    private WordService wordService;

    @Mock
    private WordReviewItemRepository wordReviewItemRepository;

    @InjectMocks
    private StudySessionService studySessionService;

    // createStudySession test

    @Test
    void testCreateStudySession() {
        // Given
        StudySessionRequestDTO requestDTO = new StudySessionRequestDTO();
        requestDTO.setGroupId(1L);
        requestDTO.setStudyActivityId(1L);

        Group group = new Group();
        group.setId(1L);

        StudyActivity activity = new StudyActivity();
        activity.setId(1L);

        when(groupService.getGroupById(requestDTO.getGroupId())).thenReturn(group);
        when(studyActivityRepository.findById(requestDTO.getStudyActivityId())).thenReturn(Optional.of(activity));

        // When
        StudySessionResponseDTO responseDTO = studySessionService.createStudySession(requestDTO);

        // Then
        assertNotNull(responseDTO);
        assertEquals(group.getId(), responseDTO.getGroupId());
        assertEquals(activity.getId(), responseDTO.getStudyActivityId());
        verify(studySessionRepository).save(any(StudySession.class));
    }

    // addReview test

    @Test
    void testAddReview() {
        // Given
        Long sessionId = 1L;
        WordReviewRequestDTO reviewDTO = new WordReviewRequestDTO();
        reviewDTO.setWordId(1L);
        reviewDTO.setCorrect(true);

        StudySession session = new StudySession();
        session.setId(sessionId);

        Word word = new Word();
        word.setId(1L);

        when(studySessionRepository.findById(sessionId)).thenReturn(Optional.of(session));
        when(wordService.getWordById(reviewDTO.getWordId())).thenReturn(word);

        // When
        WordReviewResponseDTO responseDTO = studySessionService.addReview(sessionId, reviewDTO);

        // Then
        assertNotNull(responseDTO);
        assertEquals(word.getId(), responseDTO.getWordId());
        assertEquals(sessionId, responseDTO.getSessionId());
        verify(wordReviewItemRepository).save(any(WordReviewItem.class));
    }

    // getLastStudySession

    @Test
    void testGetLastStudySession() {
        // Given
        StudySession lastSession = new StudySession();
        lastSession.setId(1L);
        lastSession.setGroup(new Group());
        lastSession.getGroup().setName("Group 1");
        lastSession.setStudyActivity(new StudyActivity());
        lastSession.getStudyActivity().setName("Activity 1");
        lastSession.setCreatedAt(LocalDateTime.now());

        when(studySessionRepository.findLatestStudySession()).thenReturn(Optional.of(lastSession));

        // Use ArrayList to create a mutable list of WordReviewItem
        List<WordReviewItem> reviews = new ArrayList<>();
        reviews.add(new WordReviewItem(true));
        reviews.add(new WordReviewItem(false));
        reviews.add(new WordReviewItem(true));

        when(wordReviewItemRepository.findByStudySessionId(lastSession.getId())).thenReturn(reviews);

        // When
        LastStudySessionResponseDTO responseDTO = studySessionService.getLastStudySession();

        // Then
        assertNotNull(responseDTO);
        assertEquals(lastSession.getId(), responseDTO.getSessionId());
        assertEquals("Group 1", responseDTO.getGroupName());
        assertEquals("Activity 1", responseDTO.getActivityName());
        assertEquals(2, responseDTO.getCorrect());
        assertEquals(1, responseDTO.getIncorrect());
    }

}