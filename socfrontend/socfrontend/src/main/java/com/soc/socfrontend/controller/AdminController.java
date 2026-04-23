package com.soc.socfrontend.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import com.soc.socfrontend.service.AuthService;

@Controller
@RequestMapping("/admin")
public class AdminController {

    private final AuthService service;

    public AdminController(AuthService service) {
        this.service = service;
    }

    @GetMapping("/pending")
    public String pendingUsers(Model model) {
        model.addAttribute("users", service.getPendingUsers());
        return "admin_pending";
    }

    @PostMapping("/approve")
    public String approve(@RequestParam Long id) {
        service.approveUser(id);
        return "redirect:/admin/pending";
    }

    @PostMapping("/reject")
    public String reject(@RequestParam Long id) {
        service.rejectUser(id);
        return "redirect:/admin/pending";
    }
}