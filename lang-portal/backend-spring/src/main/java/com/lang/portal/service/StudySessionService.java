package com.lang.portal.service;

import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.lang.portal.dto.LastStudySessionResponseDTO;
import com.lang.portal.dto.StudySessionRequestDTO;
import com.lang.portal.dto.StudySessionResponseDTO;
import com.lang.portal.dto.WordReviewRequestDTO;
import com.lang.portal.dto.WordReviewResponseDTO;
import com.lang.portal.entities.Group;
import com.lang.portal.entities.StudyActivity;
import com.lang.portal.entities.StudySession;
import com.lang.portal.entities.WordReviewItem;
import com.lang.portal.exceptions.ResourceNotFoundException;
import com.lang.portal.repository.StudyActivityRepository;
import com.lang.portal.repository.StudySessionRepository;
import com.lang.portal.repository.WordReviewItemRepository;

import lombok.RequiredArgsConstructor;

@Service
@Transactional
@RequiredArgsConstructor
public class StudySessionService {
    private final StudySessionRepository studySessionRepository;
    private final GroupService groupService;
    private final StudyActivityRepository studyActivityRepository;
    private final WordService wordService;
    private final WordReviewItemRepository wordReviewItemRepository;

    public StudySessionResponseDTO createStudySession(StudySessionRequestDTO requestDTO) {
        Group group = groupService.getGroupById(requestDTO.getGroupId());
        StudyActivity activity = studyActivityRepository.findById(requestDTO.getStudyActivityId())
                .orElseThrow(() -> new ResourceNotFoundException("StudyActivity not found"));

        StudySession session = new StudySession();
        session.setGroup(group);
        session.setStudyActivity(activity);
        studySessionRepository.save(session);

        StudySessionResponseDTO responseDTO = new StudySessionResponseDTO();
        responseDTO.setId(session.getId());
        responseDTO.setGroupId(session.getGroup().getId());
        responseDTO.setStudyActivityId(session.getStudyActivity().getId());
        responseDTO.setCreatedAt(session.getCreatedAt());

        return responseDTO;
    }

    public WordReviewResponseDTO addReview(Long sessionId, WordReviewRequestDTO reviewDTO) {
        StudySession session = studySessionRepository.findById(sessionId)
                .orElseThrow(() -> new ResourceNotFoundException("StudySession not found"));

        // Update word statistics
        wordService.updateWordStats(reviewDTO.getWordId(), reviewDTO.getCorrect());

        // Create review record
        WordReviewItem review = new WordReviewItem();
        review.setStudySession(session);
        review.setWord(wordService.getWordById(reviewDTO.getWordId()));
        review.setCorrect(reviewDTO.getCorrect());
        wordReviewItemRepository.save(review);

        var responseDTO = new WordReviewResponseDTO();
        responseDTO.setId(review.getId());
        responseDTO.setWordId(review.getWord().getId());
        responseDTO.setSessionId(review.getStudySession().getId());
        responseDTO.setCorrect(review.getCorrect());

        return responseDTO;
    }

    public LastStudySessionResponseDTO getLastStudySession() {
        StudySession lastSession = studySessionRepository.findLatestStudySession()
                .orElseThrow(() -> new ResourceNotFoundException("No study sessions found"));

        // Obtener el conteo de respuestas correctas e incorrectas
        List<WordReviewItem> reviews = wordReviewItemRepository.findByStudySessionId(lastSession.getId());
        long correctCount = reviews.stream().filter(review -> review.getCorrect()).count();
        long incorrectCount = reviews.stream().filter(review -> !review.getCorrect()).count();

        var responseDTO = new LastStudySessionResponseDTO();
        responseDTO.setSessionId(lastSession.getId());
        responseDTO.setGroupName(lastSession.getGroup().getName());
        responseDTO.setActivityName(lastSession.getStudyActivity().getName());
        responseDTO.setCorrect((int) correctCount);
        responseDTO.setIncorrect((int) incorrectCount);
        responseDTO.setCreatedAt(lastSession.getCreatedAt().toString());

        return responseDTO;
    }
}
