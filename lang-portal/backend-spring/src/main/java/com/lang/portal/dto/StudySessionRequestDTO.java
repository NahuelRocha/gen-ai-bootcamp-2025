package com.lang.portal.dto;

import lombok.Data;
import lombok.NonNull;

@Data
public class StudySessionRequestDTO {
    @NonNull
    private Long groupId;

    @NonNull
    private Long studyActivityId;

    public StudySessionRequestDTO() {
        // Default constructor
    }
}