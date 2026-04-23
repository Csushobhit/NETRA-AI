from flask import request, jsonify

from api.pipeline_service import start
from api.alert_service import get_alerts, get_by_ip
from api.ti_service import run_ti
from api.admin_service import update_env, refresh_maltrail
from api.init_indices import create_alert_index

from api.admin_routes import register_admin_routes
from api.init_admin_indices import create_audit_index
def register_routes(app):
    create_audit_index()
    register_admin_routes(app)
    create_alert_index()
    start()

    @app.route("/dashboard")
    def dashboard():
        alerts = get_alerts()

        total = len(alerts)
        suspicious = len([a for a in alerts if a["risk_score"] >= 50])
        normal = total - suspicious
        ti_malicious = len([a for a in alerts if a.get("ti_label") == "malicious"])

        # -------- TREND (last 10 alerts grouped roughly) --------
        trend = []
        for i, a in enumerate(alerts[-10:]):
            trend.append({
                "time": i,
                "total": a["risk_score"],
                "high": 1 if a["risk_score"] >= 70 else 0
            })

        # -------- DISTRIBUTION --------
        distribution = {
            "normal": normal,
            "suspicious": suspicious,
            "malicious": ti_malicious
        }

        # -------- TOP IPS --------
        ip_count = {}
        for a in alerts:
            ip = a["ip"]
            ip_count[ip] = ip_count.get(ip, 0) + 1

        top_ips = sorted(
            [{"ip": k, "count": v} for k, v in ip_count.items()],
            key=lambda x: x["count"],
            reverse=True
        )[:5]

        return jsonify({
            "total": total,
            "suspicious": suspicious,
            "normal": normal,
            "ti_malicious": ti_malicious,
            "trend": trend,
            "distribution": distribution,
            "top_ips": top_ips
        })

    @app.route("/alerts")
    def alerts():
        f = request.args.get("filter")
        h = request.args.get("hours")
        h = int(h) if h else None
        return jsonify(get_alerts(f, h))

    @app.route("/alerts/<ip>")
    def detail(ip):
        return jsonify(get_by_ip(ip))

    @app.route("/run-ti", methods=["POST"])
    def run_ti_api():
        ip = request.json.get("ip")
        return jsonify(run_ti(ip))

    @app.route("/bulk-ti", methods=["POST"])
    def bulk_ti():
        ips = request.json.get("ips", [])
        return jsonify([run_ti(ip) for ip in ips])

    @app.route("/search")
    def search():
        ip = request.args.get("ip")
        return jsonify(run_ti(ip))

    @app.route("/feedback", methods=["POST"])
    def feedback():
        from memory.store import update_feedback
        ip = request.json.get("ip")
        fb = request.json.get("feedback")
        update_feedback(ip, fb)
        return jsonify({"status": "ok"})

    @app.route("/admin/update-keys", methods=["POST"])
    def update_keys():
        return jsonify({"success": update_env(request.json)})

    @app.route("/admin/update-maltrail", methods=["POST"])
    def update_mt():
        return jsonify({"success": refresh_maltrail()})