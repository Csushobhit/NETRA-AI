from flask import request, jsonify
from api.admin_ti_service import get_all_ips, delete_ip
from api.admin_audit_service import log_action, get_logs

def register_admin_routes(app):

    @app.route("/admin/ti/<index>", methods=["GET"])
    def view_index(index):
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 50))
        search_ip = request.args.get("ip")

        data = get_all_ips(index, page, size, search_ip)

        return jsonify({
            "page": page,
            "size": size,
            "data": data
        })


    @app.route("/admin/ti/delete", methods=["POST"])
    def remove_ip():
        body = request.json

        index = body.get("index")
        ip = body.get("ip")

        success = delete_ip(index, ip)

        log_action(
            action="delete_ip",
            ip=ip,
            index=index,
            status="success" if success else "failed"
        )

        return jsonify({
            "success": success,
            "index": index,
            "ip": ip
        })


    @app.route("/admin/audit", methods=["GET"])
    def view_audit():
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 20))

        data = get_logs(page, size)

        return jsonify({
            "page": page,
            "size": size,
            "logs": data
        })