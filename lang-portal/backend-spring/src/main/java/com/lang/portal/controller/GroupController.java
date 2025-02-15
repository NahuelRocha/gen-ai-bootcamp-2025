package com.lang.portal.controller;

import org.springframework.beans.BeanUtils;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.lang.portal.dto.GroupDTO;
import com.lang.portal.dto.WordDTO;
import com.lang.portal.entities.Group;
import com.lang.portal.entities.Word;
import com.lang.portal.service.GroupService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/groups")
@RequiredArgsConstructor
public class GroupController {
    private final GroupService groupService;

    @GetMapping
    public ResponseEntity<Page<GroupDTO>> getAllGroups(
            @RequestParam(defaultValue = "1") int page) {

        Page<Group> groups = groupService.getAllGroups(page);
        Page<GroupDTO> groupDTOs = groups.map(group -> {
            GroupDTO dto = new GroupDTO();
            BeanUtils.copyProperties(group, dto);
            return dto;
        });

        return ResponseEntity.ok(groupDTOs);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Page<WordDTO>> getGroupWords(
            @PathVariable Long id,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "english") String sortBy,
            @RequestParam(defaultValue = "asc") String order) {

        Page<Word> words = groupService.getGroupWords(id, page, sortBy, order);
        Page<WordDTO> wordDTOs = words.map(word -> {
            WordDTO dto = new WordDTO();
            BeanUtils.copyProperties(word, dto);
            return dto;
        });

        return ResponseEntity.ok(wordDTOs);
    }
}
