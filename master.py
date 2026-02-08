from flask import Flask, render_template, request, jsonify, redirect
import time

app = Flask(__name__)

lobbies = {
    "SRM to Mangalagiri": {},
    "Mangalagiri to SRM": {}
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/preferences")
def preferences():
    name = request.args.get("name")
    phone = request.args.get("phone")
    dest = request.args.get("dest")

    if not name or not phone or not dest:
        return redirect("/")

    return render_template("preferences.html", name=name, phone=phone, dest=dest)

@app.route("/lobby")
def lobby():
    name = request.args.get("name")
    phone = request.args.get("phone")
    dest = request.args.get("dest")
    language = request.args.get("language")
    ride = request.args.get("ride")

    if not all([name, phone, dest, language, ride]):
        return redirect("/")

    lobbies[dest][phone] = {
        "name": name,
        "last_seen": time.time()
    }

    return render_template(
        "lobby.html",
        name=name,
        phone=phone,
        dest=dest,
        language=language,
        ride=ride
    )

@app.route("/confirmed")
def confirmed():
    phone = request.args.get("phone")
    dest = request.args.get("dest")

    # This is the "Data Reset" logic
    if dest in lobbies and phone in lobbies[dest]:
        del lobbies[dest][phone] # Remove user so they don't see "old data" next time
        
    return render_template("confirmed.html")

@app.route("/cancel")
def cancel():
    phone = request.args.get("phone")
    dest = request.args.get("dest")

    if dest in lobbies and phone in lobbies[dest]:
        del lobbies[dest][phone]

    return redirect("/")


@app.route("/api/count")
def count():
    dest = request.args.get("dest")
    phone = request.args.get("phone")

    if dest not in lobbies or phone not in lobbies[dest]:
        return jsonify({"expired": True})

    lobbies[dest][phone]["last_seen"] = time.time()

    count = len(lobbies[dest])
    fare = 220 if count == 1 else round(250 / count, 2)

    return jsonify({
        "count": count,
        "fare": fare
    })


if __name__ == "__main__":
    app.run(debug=True)
