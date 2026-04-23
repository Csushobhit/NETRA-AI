package com.soc.socfrontend.config;

import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ModelAttribute;

import java.util.HashMap;
import java.util.Map;

@ControllerAdvice
public class GlobalModelAttributes {

    @ModelAttribute
    public Map<String, Object> addGlobalAttributes(Authentication auth) {
        Map<String, Object> map = new HashMap<>();

        if (auth != null) {
            boolean isAdmin = auth.getAuthorities().stream()
                    .anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"));

            map.put("isAdmin", isAdmin);
            map.put("username", auth.getName());
        }

        return map;
    }
}