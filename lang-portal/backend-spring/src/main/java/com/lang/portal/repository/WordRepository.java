package com.lang.portal.repository;

import com.lang.portal.entities.Word;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface WordRepository extends JpaRepository<Word, Long> {

    Page<Word> findAll(Pageable pageable);

    @Query("SELECT COUNT(w) FROM Word w")
    long countTotalWords();

    @Query("SELECT COUNT(w) FROM Word w WHERE w.correctCount <> 0")
    long countWordsLearned();
}
