package com.lang.portal.repository;

import com.lang.portal.entities.StudyActivity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface StudyActivityRepository extends JpaRepository<StudyActivity, Long> {
}
