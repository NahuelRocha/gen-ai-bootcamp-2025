package com.lang.portal.repository;

import com.lang.portal.entities.StudySession;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface StudySessionRepository extends JpaRepository<StudySession, Long> {

    @Query("SELECT ss FROM StudySession ss " +
            "LEFT JOIN FETCH ss.group g " +
            "LEFT JOIN FETCH ss.studyActivity sa " +
            "WHERE ss.createdAt = (SELECT MAX(s.createdAt) FROM StudySession s)")
    Optional<StudySession> findLatestStudySession();

}
