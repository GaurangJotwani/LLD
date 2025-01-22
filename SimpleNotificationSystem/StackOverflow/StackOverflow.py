from abc import ABC, abstractmethod
from datetime import datetime
from collections import defaultdict

class Votable(ABC):
  @abstractmethod
  def vote(self, user, value):
    pass
  
  @abstractmethod
  def get_vote_count(self):
    pass

class Commentable(ABC):
  @abstractmethod
  def add_comment(self, comment):
    pass
  
  @abstractmethod
  def get_comments(self):
    pass

class Vote:
  def __init__(self, user, value):
    self.user = user
    self.value = value

class Tag:
  def __init__(self, name):
    self.id = id(self)
    self.name = name

class Question(Votable, Commentable):
  def __init__(self, author, title, content, tag_names):
    self.id = id(self)
    self.author = author
    self.title = title
    self.content = content
    self.creation_date = datetime.now()
    self.answers = []
    self.tags = [Tag(name) for name in tag_names]
    self.votes = []
    self.comments = []
  
  def add_answer(self, answer):
    if answer not in self.answers:
      self.answers.append(answer)
  
  def vote(self, user, value):
    if value not in [1,-1]:
      raise ValueError("Vote must be either 1 or -1")
    self.votes = [v for v in self.votes if v.user != user]
    self.votes.append(Vote(user, value))
    self.author.update_reputation(value * 5)
  
  def get_vote_count(self):
    return sum(v.value for v in self.votes)
  
  def add_comment(self, comment):
    self.comments.append(comment)
  
  def get_comments(self):
    return self.comments

class Answer(Votable, Commentable):
  def __init__(self, author, question, content):
    self.id = id(self)
    self.author = author
    self.question = question
    self.content = content
    self.creation_date = datetime.now()
    self.votes = []
    self.comments = []
    self.is_accepted = False
  
  def vote(self, user, value):
    if value not in [1,-1]:
      raise ValueError("Vote must be either 1 or -1")
    self.votes = [v for v in self.votes if v.user != user]
    self.votes.append(Vote(user, value))
    self.author.update_reputation(value * 10)

  def get_vote_count(self):
    return sum(v.value for v in self.votes)
  
  def add_comment(self, comment):
    self.comments.append(comment)
  
  def get_comments(self):
    return self.comments
  
  def accept(self):
    if self.is_accepted:
      return ValueError("This answer is already accepted")
    self.is_accepted = True
    self.author.update_reputation(15)

class Comment:
  def __init__(self, author, content):
    self.id = id(self)
    self.author = author
    self.content = content
    self.creation_date = datetime.now()

class User:
  def __init__(self, user_id, username, email):
    self.id = user_id
    self.username = username
    self.email = email
    self.reputation = 0
    self.questions = []
    self.answers = []
    self.comments = []
  
  def ask_question(self, title, content, tags):
    question = Question(self, title, content, tags)
    self.questions.append(question)
    self.update_reputation(5)
    return question
  
  def answer_question(self, question, content):
    answer = Answer(self, question, content)
    self.answers.append(answer)
    question.add_answer(answer)
    self.update_reputation(10)
    return answer
  
  def comment_on(self, commentable, content):
    comment = Comment(self, content)
    self.comments.append(comment)
    commentable.add_comment(comment)
    self.update_reputation(2)
  
  def update_reputation(self, value):
    self.reputation += value
    self.reputation = max(0, self.reputation)

class StackOverflow:
  def __init__(self):
    self.users = {}
    self.questions = {}
    self.answers = {}
    self.tags = {}
  
  def create_user(self, username, email):
    user_id = len(self.users) + 1
    user = User(user_id, username, email)
    self.users[user_id] = user
    return user
  
  def ask_question(self, user, title, content, tags):
    question = user.ask_question(title, content, tags)
    self.questions[question.id] = question
    for tag in question.tags:
      self.tags[tag.name] = tag
    return question
  
  def answer_question(self, user, question, content):
    answer = user.answer_question(question, content)
    self.answers[answer.id] = answer
    return answer
  
  def vote_question(self, user, question, value):
    question.vote(user, value)
  
  def vote_answer(self, user, answer, value):
    answer.vote(user, value)
  
  def accept_answer(self, answer):
    answer.accept()
  
  def search_questions(self, query):
    return [q for q in self.questions.values() if 
            query.lower() in q.title or 
            query.lower() in q.content or
            any(query.lower() == tag.name.lower() for tag in q.tags)]
  
  def get_questions_by_users(self, user):
    return user.questions
  
  def get_user(self, user_id):
    return self.users.get(user_id)
  
  def get_question(self, question_id):
    return self.questions.get(question_id)
  
  def get_answer(self, answer_id):
    return self.answers.get(answer_id)
  
  def get_tag(self, name):
    return self.tags.get(name)
  
  def add_comment(self, user, commentable, content):
    user.comment_on(commentable, content)


system = StackOverflow()

alice = system.create_user("Alice", "alice@example.com")
bob = system.create_user("Bob", "bob@example.com")
charlie = system.create_user("Charlie", "charlie@example.com")

java_question = system.ask_question(alice, "What is inheritence in Java?", "Please give example", ["java", "oop"])
bob_answer = system.answer_question(bob, java_question, "Its a technique to reduce redundancy in code")
system.add_comment(charlie, java_question, "Great question. I want to know as well")
system.add_comment(alice, bob_answer, "Thanks for the explanation! Could you provide a code example?")

# Charlie votes on the question and answer
system.vote_question(charlie, java_question, 1)  # Upvote
system.vote_answer(charlie, bob_answer, 1)  # Upvote

# Alice accepts Bob's answer
system.accept_answer(bob_answer)

# Bob asks another question
python_question = system.ask_question(bob, "How to use list comprehensions in Python?",
                                    "I'm new to Python and I've heard about list comprehensions. Can someone explain how to use them?",
                                    ["python", "list-comprehension"])

# Alice answers Bob's question
alice_answer = system.answer_question(alice, python_question,
                                    "List comprehensions in Python provide a concise way to create lists...")

# Charlie votes on Bob's question and Alice's answer
system.vote_question(charlie, python_question, 1)  # Upvote
system.vote_answer(charlie, alice_answer, 1)  # Upvote

# Print out the current state
print(f"Question: {java_question.title}")
print(f"Asked by: {java_question.author.username}")
print(f"Tags: {', '.join(tag.name for tag in java_question.tags)}")
print(f"Votes: {java_question.get_vote_count()}")
print(f"Comments: {len(java_question.get_comments())}")
print(f"\nAnswer by {bob_answer.author.username}:")
print(bob_answer.content)
print(f"Votes: {bob_answer.get_vote_count()}")
print(f"Accepted: {bob_answer.is_accepted}")
print(f"Comments: {len(bob_answer.get_comments())}")

print("\nUser Reputations:")
print(f"Alice: {alice.reputation}")
print(f"Bob: {bob.reputation}")
print(f"Charlie: {charlie.reputation}")

# Demonstrate search functionality
print("\nSearch Results for 'java':")
search_results = system.search_questions("java")
for q in search_results:
    print(q.title)

print("\nSearch Results for 'python':")
search_results = system.search_questions("python")
for q in search_results:
    print(q.title)

# Demonstrate getting questions by user
print("\nBob's Questions:")
bob_questions = system.get_questions_by_users(bob)
for q in bob_questions:
    print(q.title)

    