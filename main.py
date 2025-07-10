import random
import time
import sys
import matplotlib.pyplot as plt
from collections import deque

class MathGame:
    def __init__(self):
        self.operations = {
            '1': {'name': 'Addition', 'symbol': '+'},
            '2': {'name': 'Subtraction', 'symbol': '-'},
            '3': {'name': 'Multiplication', 'symbol': '×'},
            '4': {'name': 'Division', 'symbol': '÷'}
        }
        self.difficulties = {
            '1': {'name': '1-digit', 'min': 1, 'max': 9},
            '2': {'name': '2-digit', 'min': 10, 'max': 99},
            '3': {'name': '3-digit', 'min': 100, 'max': 999},
            '4': {'name': 'Mixed', 'min': 1, 'max': 999}
        }
        self.reset_stats()
        
    def reset_stats(self):
        self.operation = '1'
        self.difficulty = '1'
        self.score = 0
        self.rounds = 0
        self.streak = 0
        self.best_streak = 0
        self.response_times = []
        self.correct_answers = []
        self.timed_mode = False
        self.time_limit = 60  # seconds for timed mode
        
    def show_welcome(self):
        print("\n" + "="*50)
        print(" MATH PRACTICE GAME ".center(50, "="))
        print("="*50)
        print(f"\nCurrent Mode: {self.operations[self.operation]['name']} ({self.difficulties[self.difficulty]['name']} numbers)")
        print("\nCommands:")
        print("  'x' - Exit program")
        print("  'm' - Change operation mode")
        print("  'n' - Change number size preference")
        print("  's' - Show statistics")
        print("  'g' - Show performance graphs")
        print("  't' - Toggle timed challenge mode")
        print("="*50)
    
    def change_operation(self):
        print("\nSelect Operation:")
        for key, op in self.operations.items():
            print(f"  {key}. {op['name']} ({op['symbol']})")
        print("  x. Cancel")
        
        while True:
            choice = input("\nChoose operation (1-4 or x): ").lower()
            if choice == 'x':
                return
            if choice in self.operations:
                self.operation = choice
                print(f"\nOperation changed to {self.operations[choice]['name']}")
                return
            print("Invalid choice. Please enter 1-4 or x.")
    
    def change_difficulty(self):
        print("\nSelect Difficulty:")
        for key, diff in self.difficulties.items():
            print(f"  {key}. {diff['name']} numbers")
        print("  x. Cancel")
        
        while True:
            choice = input("\nChoose difficulty (1-4 or x): ").lower()
            if choice == 'x':
                return
            if choice in self.difficulties:
                self.difficulty = choice
                print(f"\nDifficulty changed to {self.difficulties[choice]['name']} numbers")
                return
            print("Invalid choice. Please enter 1-4 or x.")
    
    def generate_numbers(self):
        if self.difficulty == '4':  # Mixed difficulty
            digit_choice = random.choice(['1', '2', '3'])
            diff = self.difficulties[digit_choice]
        else:
            diff = self.difficulties[self.difficulty]
            
        num1 = random.randint(diff['min'], diff['max'])
        num2 = random.randint(diff['min'], diff['max'])
        
        # Special handling for division
        if self.operation == '4':
            if num1 < num2:
                num1, num2 = num2, num1
            if num2 == 0:
                num2 = 1
            result = random.randint(1, min(10, num1))
            num1 = num2 * result
            return num1, num2, result
        
        return num1, num2, None
    
    def generate_problem(self):
        num1, num2, forced_result = self.generate_numbers()
        op = self.operations[self.operation]
        
        if self.operation == '1':
            answer = num1 + num2
        elif self.operation == '2':
            answer = num1 - num2
        elif self.operation == '3':
            answer = num1 * num2
        elif self.operation == '4':
            answer = forced_result if forced_result else num1 // num2
        
        problem_str = f"{num1} {op['symbol']} {num2} = "
        return problem_str, answer
    
    def check_answer(self, user_answer, correct_answer):
        self.rounds += 1
        is_correct = user_answer == correct_answer
        
        if is_correct:
            self.score += 1
            self.streak += 1
            if self.streak > self.best_streak:
                self.best_streak = self.streak
            self.correct_answers.append(1)
        else:
            self.streak = 0
            self.correct_answers.append(0)
        
        return is_correct
    
    def show_stats(self):
        if self.rounds == 0:
            print("\nNo statistics available yet. Complete some problems first!")
            return
        
        accuracy = (self.score / self.rounds) * 100
        avg_time = sum(self.response_times)/len(self.response_times) if self.response_times else 0
        
        print("\n" + "="*50)
        print(" STATISTICS ".center(50, "="))
        print("="*50)
        print(f"\nOperation: {self.operations[self.operation]['name']}")
        print(f"Difficulty: {self.difficulties[self.difficulty]['name']} numbers")
        print(f"Problems Attempted: {self.rounds}")
        print(f"Correct Answers: {self.score}")
        print(f"Accuracy: {accuracy:.1f}%")
        print(f"Average Time: {avg_time:.2f}s")
        print(f"Current Streak: {self.streak}")
        print(f"Best Streak: {self.best_streak}")
        print("="*50)
        
        # Show difficulty recommendation
        if self.streak >= 5 and self.difficulty in ['1', '2']:
            print("\n⭐ You're doing great! Consider increasing difficulty!")
        elif accuracy < 50 and self.difficulty in ['2', '3', '4']:
            print("\n⚠️ You might want to try an easier difficulty level.")
    
    def plot_performance(self):
        if len(self.correct_answers) < 1:
            print("\nNot enough data to generate performance graphs yet!")
            return
        
        plt.figure(figsize=(15, 5))
        
        # Accuracy plot
        plt.subplot(1, 3, 1)
        window_size = min(10, len(self.correct_answers))
        moving_accuracy = [sum(self.correct_answers[max(0,i-window_size):i+1])/window_size*100 
                         for i in range(len(self.correct_answers))]
        plt.plot(moving_accuracy, 'g-', label=f'Last {window_size} problems')
        plt.axhline(y=(self.score/self.rounds)*100, color='r', linestyle='--', label='Overall')
        plt.title('Accuracy Over Time')
        plt.xlabel('Problem Number')
        plt.ylabel('Accuracy (%)')
        plt.ylim(0, 100)
        plt.legend()
        plt.grid(True)
        
        # Time plot
        plt.subplot(1, 3, 2)
        plt.plot(self.response_times, 'b-', label='Response Time')
        plt.axhline(y=sum(self.response_times)/len(self.response_times), 
                   color='r', linestyle='--', label='Average')
        plt.title('Response Times')
        plt.xlabel('Problem Number')
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.grid(True)
        
        # Pie chart for overall performance
        plt.subplot(1, 3, 3)
        correct = self.score
        incorrect = self.rounds - self.score
        labels = ['Correct', 'Incorrect']
        sizes = [correct, incorrect]
        colors = ['#4CAF50', '#F44336']
        explode = (0.1, 0)  # explode the correct slice
        
        if correct + incorrect > 0:
            plt.pie(sizes, explode=explode, labels=labels, colors=colors, 
                    autopct='%1.1f%%', shadow=True, startangle=90)
            plt.title('Overall Performance')
            plt.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle
        else:
            plt.text(0.5, 0.5, 'No data', ha='center', va='center')
        
        plt.tight_layout()
        plt.show()
    
    def timed_challenge(self):
        print("\n" + "="*50)
        print(" TIMED CHALLENGE ".center(50, "="))
        print("="*50)
        print(f"\nYou have {self.time_limit} seconds to solve as many problems as you can!")
        print("Type 'x' to end early")
        print("="*50)
        
        start_time = time.time()
        end_time = start_time + self.time_limit
        temp_score = 0
        temp_rounds = 0
        
        while time.time() < end_time:
            time_left = max(0, int(end_time - time.time()))
            problem, answer = self.generate_problem()
            print(f"\nTime left: {time_left}s | Problem {temp_rounds + 1}: {problem}", end="")
            
            try:
                user_input = input().strip()
                if user_input.lower() == 'x':
                    print("\nEnding timed challenge early...")
                    break
                
                user_answer = int(user_input)
            except ValueError:
                print("Please enter a valid number or 'x' to quit!")
                continue
            
            temp_rounds += 1
            is_correct = user_answer == answer
            
            if is_correct:
                temp_score += 1
                print(f"✓ Correct! ({time_left}s remaining)")
            else:
                print(f"✗ Incorrect. Answer was {answer}. ({time_left}s remaining)")
        
        # Update main statistics
        self.score += temp_score
        self.rounds += temp_rounds
        print("\n" + "="*50)
        print(" TIMED CHALLENGE RESULTS ".center(50, "="))
        print(f"\nProblems solved: {temp_rounds}")
        print(f"Correct answers: {temp_score}")
        print(f"Accuracy: {(temp_score/temp_rounds)*100 if temp_rounds > 0 else 0:.1f}%")
        print("="*50)
    
    def practice_session(self):
        self.show_welcome()
        
        while True:
            problem, answer = self.generate_problem()
            print(f"\nProblem {self.rounds + 1}: {problem}", end="", flush=True)
            
            start_time = time.time()
            user_input = input().strip().lower()
            response_time = time.time() - start_time
            
            # Process commands first
            if user_input == 'x':
                print("\nExiting practice session...")
                return 'exit'
            elif user_input == 'm':
                self.change_operation()
                self.show_welcome()
                continue
            elif user_input == 'n':
                self.change_difficulty()
                self.show_welcome()
                continue
            elif user_input == 's':
                self.show_stats()
                input("\nPress Enter to continue...")
                self.show_welcome()
                continue
            elif user_input == 'g':
                self.plot_performance()
                input("\nPress Enter to continue...")
                self.show_welcome()
                continue
            elif user_input == 't':
                self.timed_challenge()
                self.show_welcome()
                continue
            
            # Process answer
            try:
                user_answer = int(user_input)
            except ValueError:
                print("Please enter a valid number or command!")
                continue
            
            self.response_times.append(response_time)
            is_correct = self.check_answer(user_answer, answer)
            
            if is_correct:
                print(f"✓ Correct! (Time: {response_time:.2f}s)")
                if self.streak % 5 == 0:
                    print(f"🔥 Hot streak! {self.streak} correct in a row!")
            else:
                print(f"✗ Incorrect. The answer was {answer}.")
            
            print(f"Score: {self.score}/{self.rounds} | Streak: {self.streak} (Best: {self.best_streak})")
            
            # Auto-adjust difficulty
            if len(self.correct_answers) >= 5:
                recent_acc = sum(self.correct_answers[-5:])/5
                if recent_acc >= 0.8 and self.difficulty in ['1', '2']:
                    new_diff = str(int(self.difficulty) + 1)
                    print(f"\n⭐ Excellent performance! Increasing difficulty to {self.difficulties[new_diff]['name']} numbers!")
                    self.difficulty = new_diff
                elif recent_acc < 0.4 and self.difficulty in ['2', '3', '4']:
                    new_diff = str(int(self.difficulty) - 1)
                    print(f"\n⚠️ Adjusting difficulty to {self.difficulties[new_diff]['name']} numbers.")
                    self.difficulty = new_diff
    
    def run(self):
        print("\nWelcome to Math Practice!")
        print("Type 'x' at any time to exit the program")
        
        while True:
            result = self.practice_session()
            if result == 'exit':
                print("\nThank you for practicing! Goodbye!")
                sys.exit()
            
            print("\nSession ended. Would you like to:")
            print("1. Start new practice session")
            print("2. Change settings")
            print("3. Exit program")
            
            choice = input("\nEnter your choice (1-3): ").lower()
            if choice == '1':
                continue
            elif choice == '2':
                self.change_operation()
                self.change_difficulty()
            elif choice in ['3', 'x']:
                print("\nThank you for practicing! Goodbye!")
                sys.exit()
            else:
                print("Invalid choice. Please enter 1-3.")

if __name__ == "__main__":
    try:
        game = MathGame()
        game.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
        sys.exit(0)