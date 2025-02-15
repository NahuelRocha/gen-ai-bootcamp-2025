package com.lang.portal.dto;

import lombok.Data;
import lombok.NonNull;

@Data
public class WordReviewRequestDTO {
    @NonNull
    private Long wordId;

    @NonNull
    private Boolean correct;

    public WordReviewRequestDTO() {
        // Default constructor
    }
}
