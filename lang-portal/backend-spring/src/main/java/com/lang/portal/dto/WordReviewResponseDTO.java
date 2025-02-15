package com.lang.portal.dto;

import lombok.Data;

@Data
public class WordReviewResponseDTO {

    private Long id;
    private Long wordId;
    private Long sessionId;
    private Boolean correct;

}
