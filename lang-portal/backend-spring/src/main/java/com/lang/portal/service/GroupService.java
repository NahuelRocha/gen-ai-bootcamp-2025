package com.lang.portal.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.lang.portal.entities.Group;
import com.lang.portal.entities.Word;
import com.lang.portal.exceptions.ResourceNotFoundException;
import com.lang.portal.repository.GroupRepository;

import lombok.RequiredArgsConstructor;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class GroupService {
    private final GroupRepository groupRepository;

    public Page<Group> getAllGroups(int page) {
        Pageable pageable = PageRequest.of(page - 1, 10, Sort.by("name"));
        return groupRepository.findAll(pageable);
    }

    public Group getGroupById(Long id) {
        return groupRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Group not found with id: " + id));
    }

    public Page<Word> getGroupWords(Long groupId, int page, String sortBy, String order) {
        Sort.Direction direction = Sort.Direction.fromString(order.toUpperCase());
        return groupRepository.findWordsByGroupId(
                groupId,
                PageRequest.of(page - 1, 10, Sort.by(direction, sortBy)));
    }
}
