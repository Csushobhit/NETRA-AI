package com.soc.socfrontend.service;

import java.util.Arrays;
import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class BackendService {

    private final String BASE_URL = "http://localhost:9201";

    private final RestTemplate rest = new RestTemplate();

    public Map<String, Object> getDashboardStats() {
        return rest.getForObject(BASE_URL + "/dashboard", Map.class);
    }

    public List<Map<String, Object>> getAlerts(String filter, Integer hours) {
        String url = BASE_URL + "/alerts";

        if (filter != null) {
            url += "?filter=" + filter;
        }

        if (hours != null) {
            url += (url.contains("?") ? "&" : "?") + "hours=" + hours;
        }

        Map[] response = rest.getForObject(url, Map[].class);

        return Arrays.stream(response)
                .map(m -> (Map<String, Object>) m)
                .toList();
    }

    public List<Map<String, Object>> getDetails(String ip) {
        Map[] response = rest.getForObject(BASE_URL + "/alerts/" + ip, Map[].class);

        return Arrays.stream(response)
                .map(m -> (Map<String, Object>) m)
                .toList();
    }

    public Map<String, Object> runTI(String ip) {
        return rest.postForObject(BASE_URL + "/run-ti", Map.of("ip", ip), Map.class);
    }

    public List<Map<String, Object>> bulkTI(List<String> ips) {
        Map[] response = rest.postForObject(BASE_URL + "/bulk-ti", Map.of("ips", ips), Map[].class);

        return Arrays.stream(response)
                .map(m -> (Map<String, Object>) m)
                .toList();
    }

    public Map<String, Object> searchTI(String ip) {
        return rest.getForObject(BASE_URL + "/search?ip=" + ip, Map.class);
    }

    public void sendFeedback(String ip, String feedback) {
        rest.postForObject(BASE_URL + "/feedback", Map.of(
                "ip", ip,
                "feedback", feedback
        ), Map.class);
    }
}