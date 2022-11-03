from graphene import Boolean, String, Mutation, ObjectType


class TestMutation(Mutation):
    is_valid = Boolean()

    class Arguments:
        name = String()

    def mutate(self, info, **kwargs):
        return TestMutation(is_valid=True)


class UserMutation(ObjectType):
    test_mutation = TestMutation.Field()
