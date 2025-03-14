package com.kakao.sorinoon.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class KakaoMapController {

    @GetMapping("/map")
    public String getMap(Model model) {
        String KAKAO_API_KEY = "31e0f394a6fff7b5d25aaf635b5838cb";
        model.addAttribute("kakaoApiKey", KAKAO_API_KEY);
        return "map";
    }
}