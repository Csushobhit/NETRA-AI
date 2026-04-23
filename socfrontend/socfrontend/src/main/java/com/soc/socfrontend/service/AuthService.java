package com.soc.socfrontend.service;

import java.util.List;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.soc.socfrontend.model.User;
import com.soc.socfrontend.repository.UserRepository;

@Service
public class AuthService {

    private final UserRepository repo;
    private final PasswordEncoder encoder;

    public AuthService(UserRepository repo, PasswordEncoder encoder) {
        this.repo = repo;
        this.encoder = encoder;
    }

    

    public List<User> getPendingUsers() {
        return repo.findByStatus("PENDING");
    }

    public void approveUser(Long id) {
        User u = repo.findById(id).orElse(null);
        if (u != null) {
            u.setStatus("APPROVED");
            repo.save(u);
        }
    }

    public void rejectUser(Long id) {
        repo.deleteById(id);
    }

	public String register(User user) {
		if (repo.existsByUsername(user.getUsername())) {
            return "Username already exists";
        }

        if (!user.getEmail().matches("^[A-Za-z0-9+_.-]+@(.+)$")) {
            return "Invalid email";
        }

        if (!user.getPassword().matches("^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[@#$%^&+=!]).{8,}$")) {
            return "Weak password";
        }

        user.setPassword(encoder.encode(user.getPassword()));
        user.setRole("USER");
        user.setStatus("PENDING");

        repo.save(user);

        return "SUCCESS";
	}

	
}