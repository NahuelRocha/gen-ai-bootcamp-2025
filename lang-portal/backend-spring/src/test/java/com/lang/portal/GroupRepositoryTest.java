package com.lang.portal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Optional;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import com.lang.portal.entities.Group;
import com.lang.portal.repository.GroupRepository;

@SpringBootTest
@Transactional
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class GroupRepositoryTest {

    @Autowired
    private GroupRepository groupRepository;

    @Test
    void testFindGroupWithWords() {
        Group group = new Group();
        group.setName("Animals");
        group.setWordsCount(0);
        groupRepository.save(group);

        Optional<Group> foundGroup = groupRepository.findById(group.getId());
        assertTrue(foundGroup.isPresent());
        assertEquals("Animals", foundGroup.get().getName());
    }
}
