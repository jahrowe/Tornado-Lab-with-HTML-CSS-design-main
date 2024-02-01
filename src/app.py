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
            L = self.request.path.split("/")
            uname = L[2]
            info = D.get(uname)
            if info:
                self.render("profilepage.html",
                            name=info.get("name"),
                            dateOfBirth=info.get("dob"),
                            email=info.get("email"),
                            image=info.get("image")
                            )
            else:
                self.write("User not found")
        except Exception as e:
            self.set_status(500)
            self.write(f"Internal Server Error: {str(e)}")


class UpdateProfileHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            uname = self.get_argument("username", default=None)
            info = D.get(uname)
            if info:
                self.render("updateprofile.html", username=uname)
            else:
                self.write("User not found")
        except Exception as e:
            self.set_status(500)
            self.write(f"Internal Server Error: {str(e)}")


    def post(self):
        try:
            uname = self.get_argument("username", default=None)
            new_name = self.get_argument("new_name", default=None)
            new_dob = self.get_argument("new_dob", default=None)


            if uname and new_name and new_dob:
                # Update user information in the dictionary
                D[uname]["name"] = new_name
                D[uname]["dob"] = new_dob


                self.write({"success": True, "username": uname})
            else:
                self.set_status(400)  # Set status to 400 Bad Request for validation errors
                self.write({"success": False, "error": "Invalid input"})
        except Exception as e:
            self.set_status(500)
            self.write({"success": False, "error": str(e)})


def make_app():
    return tornado.web.Application([
        ("/profile/.*", ProfileHandler),
        ("/update_profile", UpdateProfileHandler),
        ("/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
    ], template_path="templates")




if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
