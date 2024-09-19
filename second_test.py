import streamlit as st
import pandas as pd

# Load the dataset
df = pd.read_csv(r'megaGymDataset.csv', index_col=0)

# Dropping duplicates and NaN values
df.drop_duplicates(inplace=True, keep='first')
df.dropna(inplace=True)

# Dropping the RatingDesc column because it has NaN or unhelpful values
df.drop(columns=["RatingDesc"], inplace=True)

# Creating a new column and imputing RatingDesc based on Rating column
def impute_rating(row):
    if row['Rating'] == 0.0:
        return 'No Rating'
    elif row['Rating'] <= 4.0:
        return 'Below Average'
    elif row['Rating'] <= 7.0:
        return 'Average'
    else:
        return 'Above Average'

df['RatingDesc'] = df.apply(lambda row: impute_rating(row), axis=1)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to set the background image
add_bg_from_local('background_image.jpg')  # Make sure the image is in the app's folder

# Dictionary to map equipment to image paths
equipment_images = {
    "Bands": "Bands.jpg",
    "Barbell": "barbell.jpg",
    "Body Only": "Body Only.jpg",
    "Barbell": "barbell.jpg",
    "Cable": "Cable Machine.jpg",
    "Dumbbell": "Dumbbell.jpg",
    "Exercise Ball": "ExerciseBall.jpg",
    "E-Z Curl Bar": "E-Z Curl Bar.jpg",
    "Foam Roll": "Foam Roll.jpg",
    "Kettlebells": "Kettlebell.jpg",
    "Machine": "Machine.jpg",
    "Medicine Ball": "Medicine Ball.jpg"
    # Add more equipment as needed
}

# Dictionary to map exercise titles to video (GIF) paths
exercise_videos = {
    "Close-grip bench press": r"bench-press-regular-bench-press.gif.mp4"
    # Add more exercise titles and their corresponding GIF paths
}

def display_video(video_path, title, width=300):
    st.write(f"**{title}**")  # Display title as caption above the video
    st.video(video_path, start_time=0)  # Use st.video to display MP4

# Functions for the different filtering options
def get_top_exercises_by_bodypart(body_part):
    df1 = df.groupby('BodyPart').apply(lambda x: x.nlargest(5, 'Rating')).reset_index(drop=True)
    filtered_df = df1[df1['BodyPart'] == body_part][['Title', 'Rating', 'BodyPart', 'RatingDesc', 'Desc', 'Level', 'Type', 'Equipment']]
    filtered_df['Sets'] = 3
    filtered_df['Reps per Set'] = 8
    return filtered_df

def get_top_exercises_by_type(exercise_type):
    df2 = df.groupby('Type').apply(lambda x: x.nlargest(5, 'Rating')).reset_index(drop=True)
    filtered_df = df2[df2['Type'] == exercise_type][['Title', 'Rating', 'BodyPart', 'Type', 'RatingDesc', 'Desc', 'Equipment', 'Level']]
    filtered_df['Sets'] = 3
    filtered_df['Reps per Set'] = 8
    return filtered_df

def get_top_exercises_by_type_and_level(exercise_type, level):
    df3 = df.groupby(['Level', 'Type']).apply(lambda x: x.nlargest(5, 'Rating')).reset_index(drop=True)
    filtered_df = df3[(df3['Type'] == exercise_type) & (df3['Level'] == level)][['Title', 'Rating', 'BodyPart', 'Type', 'RatingDesc', 'Level', 'Desc', 'Equipment']]
    filtered_df['Sets'] = 3
    filtered_df['Reps per Set'] = 8
    return filtered_df

def get_top_exercises_by_bodypart_and_level(bodypart, level):
    df3 = df.groupby(['BodyPart', 'Level']).apply(lambda x: x.nlargest(5, 'Rating')).reset_index(drop=True)
    filtered_df = df3[(df3['BodyPart'] == bodypart) & (df3['Level'] == level)][['Title', 'Rating', 'BodyPart', 'Type', 'RatingDesc', 'Level', 'Desc', 'Equipment']]
    filtered_df['Sets'] = 3
    filtered_df['Reps per Set'] = 8
    return filtered_df


# Streamlit app code
st.title("Gym and Healthy Planner")

# Dropdown menu for user input
option = st.selectbox("Choose an option", 
                      ["Filter by BodyPart", 
                       "Filter by Type", 
                       "Filter by Type and Level", 
                       "Filter by BodyPart and Level"])

# Dropdowns for the inputs
body_parts = ['Abdominals', 'Abductors', 'Biceps', 'Calves', 'Chest', 'Forearms', 'Glutes', 'Hamstrings', 'Lats', 
              'Lower Back', 'Middle Back', 'Quadriceps', 'Shoulders', 'Traps', 'Triceps']
exercise_types = ['Cardio', 'Olympic Weightlifting', 'Plyometrics', 'Powerlifting', 'Strength', 
                  'Stretching', 'Strongman']
levels = ['Beginner', 'Intermediate', 'Expert']
levels1= ['Beginner', 'Intermediate']

if option == "Filter by BodyPart":
    body_part = st.selectbox("Select BodyPart", body_parts)
    if st.button("Show Exercises"):
        result = get_top_exercises_by_bodypart(body_part)
        for index, row in result.iterrows():
            st.write(f"**Title**: {row['Title']}")
            st.write(f"**Rating**: {row['Rating']}")
            st.write(f"**BodyPart**: {row['BodyPart']}")
            st.write(f"**Type**: {row['Type']}")
            st.write(f"**Description**: {row['Desc']}")
            st.write(f"**Level**: {row['Level']}")
            st.write(f"**Equipment**: {row['Equipment']}")
            # Display image of the equipment
            if row['Equipment'] in equipment_images:
                st.image(equipment_images[row['Equipment']], caption=row['Equipment'], width=150)
            if row['Title'] in exercise_videos:
                display_video(exercise_videos[row['Title']], title=row['Title'], width=300)
            st.write(f"**Sets**: {row['Sets']} | **Reps per Set**: {row['Reps per Set']}")
            st.write("---")

elif option == "Filter by Type":
    exercise_type = st.selectbox("Select Type", exercise_types)
    if st.button("Show Exercises"):
        result = get_top_exercises_by_type(exercise_type)
        for index, row in result.iterrows():
            st.write(f"**Title**: {row['Title']}")
            st.write(f"**Rating**: {row['Rating']}")
            st.write(f"**BodyPart**: {row['BodyPart']}")
            st.write(f"**Type**: {row['Type']}")
            st.write(f"**Description**: {row['Desc']}")
            st.write(f"**Level**: {row['Level']}")
            st.write(f"**Equipment**: {row['Equipment']}")
            # Display image of the equipment
            if row['Equipment'] in equipment_images:
                st.image(equipment_images[row['Equipment']], caption=row['Equipment'], width=150)
            if row['Title'] in exercise_videos:
                display_video(exercise_videos[row['Title']], title=row['Title'], width=300)
            st.write(f"**Sets**: {row['Sets']} | **Reps per Set**: {row['Reps per Set']}")
            st.write("---")

elif option == "Filter by Type and Level":
    exercise_type = st.selectbox("Select Type", exercise_types)
    level = st.selectbox("Select Level", levels)
    if st.button("Show Exercises"):
        result = get_top_exercises_by_type_and_level(exercise_type, level)
        for index, row in result.iterrows():
            st.write(f"**Title**: {row['Title']}")
            st.write(f"**Rating**: {row['Rating']}")
            st.write(f"**BodyPart**: {row['BodyPart']}")
            st.write(f"**Type**: {row['Type']}")
            st.write(f"**Level**: {row['Level']}")
            st.write(f"**Description**: {row['Desc']}")
            st.write(f"**Equipment**: {row['Equipment']}")
            # Display image of the equipment
            if row['Equipment'] in equipment_images:
                st.image(equipment_images[row['Equipment']], caption=row['Equipment'], width=150)
            if row['Title'] in exercise_videos:
                display_video(exercise_videos[row['Title']], title=row['Title'], width=300)
            st.write(f"**Sets**: {row['Sets']} | **Reps per Set**: {row['Reps per Set']}")
            st.write("---")

elif option == "Filter by BodyPart and Level":
    body_part = st.selectbox("Select BodyPart", body_parts)
    level = st.selectbox("Select Level", levels1)
    if st.button("Show Exercises"):
        result = get_top_exercises_by_bodypart_and_level(body_part, level)
        for index, row in result.iterrows():
            st.write(f"**Title**: {row['Title']}")
            st.write(f"**Rating**: {row['Rating']}")
            st.write(f"**BodyPart**: {row['BodyPart']}")
            st.write(f"**Type**: {row['Type']}")
            st.write(f"**Level**: {row['Level']}")
            st.write(f"**Description**: {row['Desc']}")
            st.write(f"**Equipment**: {row['Equipment']}")
            # Display image of the equipment
            if row['Equipment'] in equipment_images:
                st.image(equipment_images[row['Equipment']], caption=row['Equipment'], width=150)
            if row['Title'] in exercise_videos:
                display_video(exercise_videos[row['Title']], title=row['Title'], width=300)
            st.write(f"**Sets**: {row['Sets']} | **Reps per Set**: {row['Reps per Set']}")
            st.write("---")
