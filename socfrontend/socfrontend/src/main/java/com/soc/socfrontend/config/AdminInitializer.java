package com.soc.socfrontend.config;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.password.PasswordEncoder;

import com.soc.socfrontend.model.User;
import com.soc.socfrontend.repository.UserRepository;

@Configuration
public class AdminInitializer {

    @Bean
    CommandLineRunner initAdmin(UserRepository repo, PasswordEncoder encoder) {
        return args -> {
            if (!repo.existsByUsername("admin")) {
                User admin = new User(
                        "Admin",
                        "admin",
                        "admin@soc.com",
                        encoder.encode("admin@123"),
                        "ADMIN",
                        "APPROVED"
                );
                repo.save(admin);
            }
        };
    }
}