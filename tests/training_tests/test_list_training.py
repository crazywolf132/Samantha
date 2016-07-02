# -*- coding: utf-8 -*-
from tests.base_case import SamanthaTestCase
from samantha.training.trainers import ListTrainer


class ListTrainingTests(SamanthaTestCase):

    def setUp(self):
        super(ListTrainingTests, self).setUp()
        self.Samantha.set_trainer(ListTrainer)

    def test_training_adds_statements(self):
        """
        Test that the training method adds statements
        to the database.
        """
        conversation = [
            "Hello",
            "Hi there!",
            "How are you doing?",
            "I'm great.",
            "That is good to hear",
            "Thank you.",
            "You are welcome.",
            "Sure, any time.",
            "Yeah",
            "Can I help you with anything?"
        ]

        self.Samantha.train(conversation)

        response = self.Samantha.get_response("Thank you.")

        self.assertEqual(response, "You are welcome.")

    def test_training_increments_occurrence_count(self):

        conversation = [
            "Do you like my hat?",
            "I do not like your hat."
        ]

        self.Samantha.train(conversation)
        self.Samantha.train(conversation)

        statements = self.Samantha.storage.filter(
            in_response_to__contains="Do you like my hat?"
        )
        response = statements[0].in_response_to[0]

        self.assertEqual(response.occurrence, 2)

    def test_database_has_correct_format(self):
        """
        Test that the database maintains a valid format
        when data is added and updated. This means that
        after the training process, the database should
        contain nine objects and eight of these objects
        should list the previous member of the list as
        a response.
        """
        conversation = [
            "Hello sir!",
            "Hi, can I help you?",
            "Yes, I am looking for italian parsely.",
            "Italian parsely is right over here in out produce department",
            "Great, thank you for your help.",
            "No problem, did you need help finding anything else?",
            "Nope, that was it.",
            "Alright, have a great day.",
            "Thanks, you too."
        ]

        self.Samantha.train(conversation)

        # There should be a total of 9 statements in the database after training
        self.assertEqual(self.Samantha.storage.count(), 9)

        # The first statement should be in responce to another statement yet
        self.assertEqual(
            len(self.Samantha.storage.find(conversation[0]).in_response_to),
            0
        )

        # The second statement should have one response
        self.assertEqual(
            len(self.Samantha.storage.find(conversation[1]).in_response_to),
            1
        )

        # The second statement should be in response to the first statement
        self.assertIn(
            conversation[0],
            self.Samantha.storage.find(conversation[1]).in_response_to,
        )

    def test_training_with_unicode_characters(self):
        """
        Ensure that the training method adds unicode statements
        to the database.
        """
        conversation = [
            u"¶ ∑ ∞ ∫ π ∈ ℝ² ∖ ⩆ ⩇ ⩈ ⩉ ⩊ ⩋ ⪽ ⪾ ⪿ ⫀ ⫁ ⫂ ⋒ ⋓",
            u"⊂ ⊃ ⊆ ⊇ ⊈ ⊉ ⊊ ⊋ ⊄ ⊅ ⫅ ⫆ ⫋ ⫌ ⫃ ⫄ ⫇ ⫈ ⫉ ⫊ ⟃ ⟄",
            u"∠ ∡ ⦛ ⦞ ⦟ ⦢ ⦣ ⦤ ⦥ ⦦ ⦧ ⦨ ⦩ ⦪ ⦫ ⦬ ⦭ ⦮ ⦯ ⦓ ⦔ ⦕ ⦖ ⟀",
            u"∫ ∬ ∭ ∮ ∯ ∰ ∱ ∲ ∳ ⨋ ⨌ ⨍ ⨎ ⨏ ⨐ ⨑ ⨒ ⨓ ⨔ ⨕ ⨖ ⨗ ⨘ ⨙ ⨚ ⨛ ⨜",
            u"≁ ≂ ≃ ≄ ⋍ ≅ ≆ ≇ ≈ ≉ ≊ ≋ ≌ ⩯ ⩰ ⫏ ⫐ ⫑ ⫒ ⫓ ⫔ ⫕ ⫖",
            u"¬ ⫬ ⫭ ⊨ ⊭ ∀ ∁ ∃ ∄ ∴ ∵ ⊦ ⊬ ⊧ ⊩ ⊮ ⊫ ⊯ ⊪ ⊰ ⊱ ⫗ ⫘",
            u"∧ ∨ ⊻ ⊼ ⊽ ⋎ ⋏ ⟑ ⟇ ⩑ ⩒ ⩓ ⩔ ⩕ ⩖ ⩗ ⩘ ⩙ ⩚ ⩛ ⩜ ⩝ ⩞ ⩟ ⩠ ⩢",
        ]

        self.Samantha.train(conversation)

        response = self.Samantha.get_response(conversation[1])

        self.assertEqual(response, conversation[2])

    def test_similar_sentence_gets_same_response_multiple_times(self):
        """
        Tests if the bot returns the same response for the same question (which
        is similar to the one present in the training set) when asked repeatedly.
        """
        training = [
            'how do you login to gmail?',
            'Goto gmail.com, enter your login information and hit enter!'
        ]

        similar_question = 'how do I login to gmail?'

        self.Samantha.train(training)

        response_to_trained_set = self.Samantha.get_response('how do you login to gmail?')
        response_to_similar_question_1 = self.Samantha.get_response(similar_question)
        response_to_similar_question_2 = self.Samantha.get_response(similar_question)

        self.assertEqual(response_to_trained_set, response_to_similar_question_1)
        self.assertEqual(response_to_similar_question_1, response_to_similar_question_2)


class samanthaResponseTests(SamanthaTestCase):

    def setUp(self):
        super(samanthaResponseTests, self).setUp()
        """
        Set up a database for testing.
        """
        self.Samantha.set_trainer(ListTrainer)

        data1 = [
            "african or european?",
            "Huh? I... I don't know that.",
            "How do you know so much about swallows?"
        ]

        data2 = [
            "Siri is adorable",
            "Who is Seri?",
            "Siri is my cat"
        ]

        data3 = [
            "What... is your quest?",
            "To seek the Holy Grail.",
            "What... is your favourite colour?",
            "Blue."
        ]

        self.Samantha.train(data1)
        self.Samantha.train(data2)
        self.Samantha.train(data3)

    def test_answer_to_known_input(self):
        """
        Test that a matching response is returned
        when an exact match exists.
        """
        input_text = "What... is your favourite colour?"
        response = self.Samantha.get_response(input_text)

        self.assertIn("Blue", response)

    def test_answer_close_to_known_input(self):

        input_text = "What is your favourite colour?"
        response = self.Samantha.get_response(input_text)

        self.assertIn("Blue", response)

    def test_match_has_no_response(self):
        """
        Make sure that the if the last line in a file
        matches the input text then a index error does
        not occure.
        """
        input_text = "Siri is my cat"
        response = self.Samantha.get_response(input_text)

        self.assertGreater(len(response), 0)

    def test_empty_input(self):
        """
        If empty input is provided, anything may be returned.
        """
        output = self.Samantha.get_response("")

        self.assertTrue(len(output) >= 0)

