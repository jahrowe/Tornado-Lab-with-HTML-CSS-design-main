import tornado.web
import tornado.ioloop

D = {
    "alice": {"name": "Alice Smith", "dob": "Jan. 1", "email": "alice@example.com", "image": "/static/alice.jpg"},
    "bob": {"name": "Bob Jones", "dob": "Dec. 31", "email": "bob@bob.xyz", "image": "/static/bob.jpg"},
    "carol": {"name": "Carol Ling", "dob": "Jul. 17", "email": "carol@example.com", "image": "/static/carol.jpg"},
    "dave": {"name": "Dave N. Port", "dob": "Mar. 14", "email": "dave@dave.dave", "image": "/static/dave.jpg"},
}


class ProfileHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            uname = self.get_username_from_path()
            info = D.get(uname)
            
            if info:
                self.render("profilepage.html",
                            username=uname,  # Pass username to the template
                            name=info.get("name"),
                            dateOfBirth=info.get("dob"),
                            email=info.get("email"),
                            image=info.get("image"))
            else:
                # If user not found, return a 404 error
                self.set_status(404)
                self.write("User not found")
        except Exception as e:
            # Handle internal server errors gracefully
            self.set_status(500)
            self.write(f"Internal Server Error: {str(e)}")

    def get_username_from_path(self):
        # Split the URL path and extract the username
        parts = self.request.path.split("/")
        return parts[2] if len(parts) > 2 else None

    def render_profile(self, info):
        # Render the profile page template with user data
        self.render("profilepage.html",
                    name=info.get("name"),
                    dateOfBirth=info.get("dob"),
                    email=info.get("email"),
                    image=info.get("image"))


class UpdateProfileHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            uname = data.get("username")  
            new_name = data.get("new_name")
            new_dob = data.get("new_dob")

            if uname and new_name and new_dob:
                # Update user information in the dictionary
                D[uname]["name"] = new_name
                D[uname]["dob"] = new_dob
                self.write({"success": True})
            else:
                self.set_status(400)  # Set status to 400 Bad Request for validation errors
                self.write({"success": False, "error": "Invalid input"})
        
        except Exception as e:
            self.set_status(500)
            self.write({"success": False, "error": str(e)})


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome!")

def make_app():
    return tornado.web.Application([
        ("/", MainHandler),
        ("/profile/.*", ProfileHandler),
        ("/updateprofile", UpdateProfileHandler),
        ("/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
    ], template_path="templates")


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
    