from flask_graphql import GraphQLView


class MyCustomGraphQLView(GraphQLView):
    def dispatch_request(self):
        response = super(MyCustomGraphQLView, self).dispatch_request()

        cookie_session = self.get_context().get("cookie_session")
        if "set_cookie" in cookie_session:
            response.headers["Set-Cookie"] = cookie_session.get("set_cookie")
        cookie_session.clear()

        return response
