package com.lang.portal.repository;

import com.lang.portal.entities.Group;
import com.lang.portal.entities.Word;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface GroupRepository extends JpaRepository<Group, Long> {

    Page<Group> findAll(Pageable pageable);

    @Query("SELECT w FROM Word w JOIN w.groups g WHERE g.id = :groupId")
    Page<Word> findWordsByGroupId(@Param("groupId") Long groupId, Pageable pageable);
}
