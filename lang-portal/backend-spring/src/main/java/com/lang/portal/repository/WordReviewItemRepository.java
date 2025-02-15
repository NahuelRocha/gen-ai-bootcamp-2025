package com.lang.portal.repository;

import com.lang.portal.entities.WordReviewItem;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface WordReviewItemRepository extends JpaRepository<WordReviewItem, Long> {

    List<WordReviewItem> findByStudySessionId(Long studySessionId);
}