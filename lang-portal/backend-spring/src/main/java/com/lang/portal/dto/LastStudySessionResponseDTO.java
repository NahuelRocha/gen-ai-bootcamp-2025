package com.lang.portal.dto;

import lombok.Data;

@Data
public class LastStudySessionResponseDTO {
    private Long sessionId;
    private String groupName;
    private String activityName;
    private Integer correct;
    private Integer incorrect;
    private String createdAt;
}
