package com.lang.portal.dto;

import java.time.LocalDateTime;

import lombok.Data;

@Data
public class StudySessionResponseDTO {
    private Long id;
    private Long groupId;
    private Long studyActivityId;
    private LocalDateTime createdAt;
}
