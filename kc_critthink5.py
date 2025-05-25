from collections import defaultdict

# Dictionary to store user preferences
# Each user has a list of liked and disliked post IDs
users = {
    1: {'liked': [101, 102], 'disliked': [103]},
    2: {'liked': [101, 104], 'disliked': []},
    3: {'liked': [102, 105], 'disliked': [101]},
}

# Dictionary to store content details
# Each post has a title and associated tags
content = {
    101: {'title': 'Post A', 'tags': ['funny', 'viral']},
    102: {'title': 'Post B', 'tags': ['informative', 'news']},
    103: {'title': 'Post C', 'tags': ['advertisement']},
    104: {'title': 'Post D', 'tags': ['funny', 'meme']},
    105: {'title': 'Post E', 'tags': ['news', 'update']},
}

# Precompute a mapping from tags to content IDs for efficient lookups
tagToContent = defaultdict(set)
for postID, details in content.items():
    for tag in details['tags']:
        tagToContent[tag].add(postID)

def recommendContent(userID, users, content):
    # Check if the user exists in the users dictionary
    if userID not in users:
        return "User  not found."

    # Retrieve liked and disliked content for the user
    likedContent = users[userID]['liked']
    dislikedContent = set(users[userID]['disliked'])
    likedTags = set()

    # Collect all tags from the content that the user has liked
    for postID in likedContent:
        if postID in content:
            likedTags.update(content[postID]['tags'])

    recommendations = set()

    # Recommend content that shares tags with liked content
    # Exclude posts that the user has already liked or disliked
    for tag in likedTags:
        for postID in tagToContent[tag]:
            if postID not in likedContent and postID not in dislikedContent:
                recommendations.add(postID)

    # Return the titles of the recommended posts
    return [content[postID]['title'] for postID in recommendations]

def updateUserPreferences(userID, actions):
    # Check if the user exists in the users dictionary
    if userID in users:
        # Process each action (like or dislike) for the specified post IDs
        for action, postID in actions:
            if action == 'like':
                # Add postID to liked list if not already liked
                if postID not in users[userID]['liked']:
                    users[userID]['liked'].append(postID)
                    print(f"User  {userID} liked Post ID {postID}: '{content[postID]['title']}'")
                # Remove postID from disliked list if it was previously disliked
                if postID in users[userID]['disliked']:
                    users[userID]['disliked'].remove(postID)
                    print(f"User  {userID} removed Post ID {postID} from dislikes.")
            elif action == 'dislike':
                # Add postID to disliked list if not already disliked
                if postID not in users[userID]['disliked']:
                    users[userID]['disliked'].append(postID)
                    print(f"User  {userID} disliked Post ID {postID}: '{content[postID]['title']}'")
                # Remove postID from liked list if it was previously liked
                if postID in users[userID]['liked']:
                    users[userID]['liked'].remove(postID)
                    print(f"User  {userID} removed Post ID {postID} from likes.")

if __name__ == "__main__":
    userID = 1
    # Get recommendations for the specified user
    recommendedPosts = recommendContent(userID, users, content)
    print(f"Recommended posts for User {userID}: {recommendedPosts if recommendedPosts else 'No recommendations available.'}")

    # Simulate real-time updates - user likes posts 104 and 105
    updateUserPreferences(userID, [('like', 104), ('like', 105)])
    # Get updated recommendations after the user has liked new posts
    recommendedPosts = recommendContent(userID, users, content)
    print(f"Updated recommendations for User {userID}: {recommendedPosts if recommendedPosts else 'No recommendations available.'}")