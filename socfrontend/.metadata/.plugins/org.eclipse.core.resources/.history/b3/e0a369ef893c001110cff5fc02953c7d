package com.soc.socfrontend.service;

import java.util.Map;
import java.util.List;
import java.util.Arrays;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class AdminService {

    private final String BASE = "http://localhost:9201";
    private final RestTemplate rest = new RestTemplate();

    public Map getTIIndex(String index) {
        return rest.getForObject(BASE + "/admin/ti/" + index, Map.class);
    }

    public Map deleteIP(String index, String ip) {
        return rest.postForObject(BASE + "/admin/ti/delete",
                Map.of("index", index, "ip", ip),
                Map.class);
    }

    public Map getAudit() {
        return rest.getForObject(BASE + "/admin/audit", Map.class);
    }

    public Map updateKeys(Map body) {
        return rest.postForObject(BASE + "/admin/update-keys", body, Map.class);
    }

    public Map updateMaltrail() {
        return rest.postForObject(BASE + "/admin/update-maltrail", null, Map.class);
    }
}