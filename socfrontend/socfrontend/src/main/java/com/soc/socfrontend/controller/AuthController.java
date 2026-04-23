package com.soc.socfrontend.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import com.soc.socfrontend.model.User;
import com.soc.socfrontend.service.AuthService;

@Controller
public class AuthController {

    private final AuthService service;

    public AuthController(AuthService service) {
        this.service = service;
    }

    @GetMapping("/auth")
    public String authPage(Model model) {
        model.addAttribute("user", new User());
        return "auth";
    }

    @PostMapping("/register")
    public String register(@ModelAttribute User user, Model model) {

        String result = service.register(user);

        if (!"SUCCESS".equals(result)) {
            model.addAttribute("error", result);
            model.addAttribute("user", new User());
            return "auth";
        }

        model.addAttribute("message", "Signup successful. Wait for admin approval.");
        model.addAttribute("user", new User());
        return "auth";
    }

    @GetMapping("/login")
    public String loginRedirect() {
        return "auth";
    }
}