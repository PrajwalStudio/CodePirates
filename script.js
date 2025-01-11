// Fetch posts from Flask backend (using Fetch API)
const fetchPosts = async () => {
    try {
        const response = await fetch('http://localhost:5000/api/posts');
        const posts = await response.json();
        
        const feedSection = document.getElementById('feed');
        feedSection.innerHTML = '';  // Clear the feed section
        posts.forEach(post => {
            const postElement = document.createElement('div');
            postElement.classList.add('post');
            postElement.innerHTML = `
                <h3>${post.user}</h3>
                <p>${post.content}</p>
            `;
            feedSection.appendChild(postElement);
        });
    } catch (error) {
        console.error('Error fetching posts', error);
    }
};

window.onload = () => {
    fetchPosts();
};
