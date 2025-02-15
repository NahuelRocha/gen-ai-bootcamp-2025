package com.lang.portal.dto;

import lombok.Data;

@Data
public class WordDTO {
    private Long id;
    private String english;
    private String spanish;
    private String pronunciation;
    private String parts;
    private Integer correctCount;
    private Integer wrongCount;
}
