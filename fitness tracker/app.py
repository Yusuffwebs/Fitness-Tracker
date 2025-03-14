from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

exercises_file = "exercises.txt"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/main_tracking', methods=['GET', 'POST'])
def main_tracking():
    if request.method == 'POST':
        exercise = request.form.get('exercise')
        duration = request.form.get('duration')
        date = request.form.get('date')
        calories_burned = calculate_calories(exercise, int(duration))

        with open(exercises_file, 'a') as f:
            f.write(f"{date}, {exercise}, {duration}, {calories_burned}\n")

    workouts = get_workouts()
    total_workouts = len(workouts)
    total_duration = sum([w['duration'] for w in workouts])
    total_calories = sum([w['calories_burned'] for w in workouts])

    avg_duration = total_duration / total_workouts if total_workouts else 0
    avg_calories = total_calories / total_workouts if total_workouts else 0

    return render_template(
        'main_tracking.html',
        workouts=workouts,
        total_workouts=total_workouts,
        total_duration=total_duration,
        total_calories=total_calories,
        avg_duration=avg_duration,
        avg_calories=avg_calories,
    )


@app.route('/diet_plan')
def diet_plan():
    return render_template('diet_plan.html')


@app.route('/delete_workout/<int:workout_index>', methods=['POST'])
def delete_workout(workout_index):
    workouts = get_workouts()
    if 0 <= workout_index < len(workouts):
        workouts.pop(workout_index)
        save_workouts(workouts)
    return redirect(url_for('main_tracking'))


def calculate_calories(exercise, duration):
    calories = 0
    if exercise == 'Running':
        calories = duration * 10
    elif exercise in ['Cycling', 'Swimming', 'Weightlifting']:
        calories = duration * 5
    else:
        calories = duration * 3
    return calories

def get_workouts():
    workouts = []
    if os.path.exists(exercises_file):
        with open(exercises_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                date, exercise, duration, calories_burned = line.strip().split(', ')
                workouts.append({
                    'date': date,
                    'exercise': exercise,
                    'duration': int(duration),
                    'calories_burned': int(calories_burned)
                })
    return workouts


def save_workouts(workouts):
    with open(exercises_file, 'w') as f:
        for workout in workouts:
            f.write(f"{workout['date']}, {workout['exercise']}, {workout['duration']}, {workout['calories_burned']}\n")

if __name__ == '__main__':
    app.run(debug=True)