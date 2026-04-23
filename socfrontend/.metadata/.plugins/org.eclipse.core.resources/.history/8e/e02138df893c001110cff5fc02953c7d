package com.soc.socfrontend.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import com.soc.socfrontend.service.AdminService;

import java.util.Map;

@Controller
@RequestMapping("/admin-ui")
public class AdminUIController {

    private final AdminService service;

    public AdminUIController(AdminService service) {
        this.service = service;
    }

    @GetMapping("/ti")
    public String tiIndex(@RequestParam(defaultValue = "known_malicious_ips") String index,
                          Model model) {

        Map res = service.getTIIndex(index);

        model.addAttribute("data", res.get("data"));
        model.addAttribute("index", index);

        return "admin_ti";
    }

    @PostMapping("/delete")
    public String delete(@RequestParam String index, @RequestParam String ip) {
        service.deleteIP(index, ip);
        return "redirect:/admin-ui/ti?index=" + index;
    }

    @GetMapping("/audit")
    public String audit(Model model) {
        Map res = service.getAudit();
        model.addAttribute("logs", res.get("logs"));
        return "admin_audit";
    }

    @GetMapping("/keys")
    public String keysPage() {
        return "admin_keys";
    }

    @PostMapping("/keys")
    public String updateKeys(@RequestParam Map<String, String> body) {
        service.updateKeys(body);
        return "redirect:/admin-ui/keys";
    }

    @PostMapping("/maltrail")
    public String refresh() {
        service.updateMaltrail();
        return "redirect:/admin-ui/ti";
    }
}