package com.lang.portal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import com.lang.portal.controller.StudySessionController;
import com.lang.portal.dto.LastStudySessionResponseDTO;
import com.lang.portal.dto.StudySessionRequestDTO;
import com.lang.portal.dto.StudySessionResponseDTO;
import com.lang.portal.dto.WordReviewRequestDTO;
import com.lang.portal.dto.WordReviewResponseDTO;
import com.lang.portal.service.StudySessionService;

import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
public class StudySessionControllerTest {

    @Mock
    private StudySessionService studySessionService;

    @InjectMocks
    private StudySessionController studySessionController;

    @Test
    void testCreateStudySession() {
        StudySessionRequestDTO requestDTO = new StudySessionRequestDTO();
        requestDTO.setGroupId(1L); // Ajusta según los campos de tu DTO

        StudySessionResponseDTO responseDTO = new StudySessionResponseDTO();
        responseDTO.setId(1L); // Ajusta según los campos de tu DTO

        when(studySessionService.createStudySession(requestDTO)).thenReturn(responseDTO);

        ResponseEntity<StudySessionResponseDTO> response = studySessionController.createStudySession(requestDTO);

        assertNotNull(response);
        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(1L, response.getBody().getId()); // Ajusta según los campos de tu DTO

        verify(studySessionService, times(1)).createStudySession(requestDTO);
    }

    @Test
    void testAddReview() {
        Long sessionId = 1L;
        WordReviewRequestDTO reviewDTO = new WordReviewRequestDTO();
        reviewDTO.setWordId(1L);
        reviewDTO.setCorrect(true);

        WordReviewResponseDTO responseDTO = new WordReviewResponseDTO();
        responseDTO.setCorrect(true);

        when(studySessionService.addReview(sessionId, reviewDTO)).thenReturn(responseDTO);

        ResponseEntity<WordReviewResponseDTO> response = studySessionController.addReview(sessionId, reviewDTO);

        assertNotNull(response);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(true, response.getBody().getCorrect()); // Ajusta según los campos de tu DTO

        verify(studySessionService, times(1)).addReview(sessionId, reviewDTO);
    }

    @Test
    void testGetLastStudySession() {
        LastStudySessionResponseDTO responseDTO = new LastStudySessionResponseDTO();
        responseDTO.setActivityName("value"); // Ajusta según los campos de tu DTO

        when(studySessionService.getLastStudySession()).thenReturn(responseDTO);

        ResponseEntity<LastStudySessionResponseDTO> response = studySessionController.getLastStudySession();

        assertNotNull(response);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("value", response.getBody().getActivityName()); // Ajusta según los campos de tu DTO

        verify(studySessionService, times(1)).getLastStudySession();
    }
}
