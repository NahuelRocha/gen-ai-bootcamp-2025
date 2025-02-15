package com.lang.portal.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.lang.portal.dto.LastStudySessionResponseDTO;
import com.lang.portal.dto.StudySessionRequestDTO;
import com.lang.portal.dto.StudySessionResponseDTO;
import com.lang.portal.dto.WordReviewRequestDTO;
import com.lang.portal.dto.WordReviewResponseDTO;
import com.lang.portal.service.StudySessionService;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/study_sessions")
@RequiredArgsConstructor
public class StudySessionController {
    private final StudySessionService studySessionService;

    @PostMapping
    public ResponseEntity<StudySessionResponseDTO> createStudySession(
            @Valid @RequestBody StudySessionRequestDTO requestDTO) {
        var session = studySessionService.createStudySession(requestDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(session);
    }

    @PostMapping("/{id}/review")
    public ResponseEntity<WordReviewResponseDTO> addReview(
            @PathVariable Long id,
            @Valid @RequestBody WordReviewRequestDTO reviewDTO) {

        var review = studySessionService.addReview(id, reviewDTO);
        return ResponseEntity.ok(review);
    }

    @GetMapping("/last")
    public ResponseEntity<LastStudySessionResponseDTO> getLastStudySession() {
        LastStudySessionResponseDTO response = studySessionService.getLastStudySession();
        return ResponseEntity.ok(response);
    }
}
