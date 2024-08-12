// Function that runs once the window is fully loaded
window.onload = function() {
    // Attempt to retrieve the API base URL from the local storage
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    // If a base URL is found in local storage, load the posts
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
}

// Function to fetch all the posts from the API and display them on the page
function loadPosts() {
    const baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);
    // Add sorting elements
    const sortContainer = document.createElement('div');
    sortContainer.classList.add('sort-container');

    const sortBySelect = document.createElement('select');
    sortBySelect.id = 'sort-by';
    sortBySelect.innerHTML = `
        <option value="">Sort By</option>
        <option value="title">Title</option>
        <option value="date">Date</option>
        <option value="author">Author</option>
        <option value="content">Content</option>
    `;
    const directionSort = document.createElement('select')
    directionSort.id = 'direction-to'
    directionSort.innerHTML = `
        <option value="">Default</option>
        <option value="desc">desc</option>
        <option value="asc">asc</option>
    `

    const sortButton = document.createElement('button');
    sortButton.id = 'sort-button';
    sortButton.textContent = 'Sort';

    sortContainer.appendChild(sortBySelect);
    sortContainer.appendChild(directionSort);
    sortContainer.appendChild(sortButton);

    document.getElementById('post-container').parentNode.insertBefore(sortContainer, document.getElementById('post-container'));
    
    fetch(baseUrl + '/posts')
      .then(response => response.json())
      .then(data => {
        const postContainer = document.getElementById('post-container');
        postContainer.innerHTML = '';
  
        data.forEach(post => {
          const postDiv = document.createElement('div');
          postDiv.className = 'post';
          postDiv.innerHTML = `<h2>${post.title}</h2><p class="header">${post.author}</p><p>${post.content}</p>`;
  
          const buttonDiv = document.createElement('div');
          buttonDiv.className = 'button-container';
  
          const deleteButton = document.createElement('button');
          deleteButton.className = 'button';
          deleteButton.textContent = 'Delete';
          deleteButton.onclick = () => deletePost(post.id);
  
          const updateButton = document.createElement('button');
          updateButton.className = 'button';
          updateButton.textContent = 'Update';
          updateButton.addEventListener('click', () => {
            const updateForm = createUpdateForm(post); // Use a function to create the update form
            postDiv.appendChild(updateForm);
            updateForm.style.display = 'block';
          });
  
          buttonDiv.appendChild(deleteButton);
          buttonDiv.appendChild(updateButton);
          postDiv.appendChild(buttonDiv);
          postContainer.appendChild(postDiv);
        });
        sortButton.addEventListener('click', () => {
            const sortBy = sortBySelect.value;
            const directionTo = directionSort.value
            const sortedPostsUrl = `${baseUrl}/posts?sort=${sortBy}&direction=${directionTo}`; // Modify URL based on your backend logic
            fetch(sortedPostsUrl)
              .then(response => response.json())
              .then(sortedData => {
                displayPosts(sortedData); // Update UI with sorted posts
              })
              .catch(error => console.error('Error:', error));
          });
      })
      .catch(error => console.error('Error:', error));
}

// Function for displaying sorted posts
function displayPosts(posts) {
    const postContainer = document.getElementById('post-container');
    postContainer.innerHTML = '';
  
    posts.forEach(post => {
        const postDiv = document.createElement('div');
        postDiv.className = 'post';
        postDiv.innerHTML = `<h2>${post.title}</h2><p class="header">${post.author}</p><p>${post.content}</p>`;

        const buttonDiv = document.createElement('div');
        buttonDiv.className = 'button-container';

        const deleteButton = document.createElement('button');
        deleteButton.className = 'button';
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = () => deletePost(post.id);

        const updateButton = document.createElement('button');
        updateButton.className = 'button';
        updateButton.textContent = 'Update';
        updateButton.addEventListener('click', () => {
          const updateForm = createUpdateForm(post); // Use a function to create the update form
          postDiv.appendChild(updateForm);
          updateForm.style.display = 'block';
        });

        buttonDiv.appendChild(deleteButton);
        buttonDiv.appendChild(updateButton);
        postDiv.appendChild(buttonDiv);
        postContainer.appendChild(postDiv);
    });
}

// Function to create the update form (cleaner and reusable)
function createUpdateForm(post) {
    const updateForm = document.createElement('div');
    updateForm.className = 'update-form';
  
    const titleInput = document.createElement('input');
    titleInput.type = 'text';
    titleInput.name = 'title';
    titleInput.placeholder = 'Enter new title';
    titleInput.value = post.title;
  
    const contentInput = document.createElement('textarea');
    contentInput.name = 'content';
    contentInput.placeholder = 'Enter new content';
    contentInput.value = post.content;
  
    const submitButton = document.createElement('button');
    submitButton.textContent = 'Save';
    submitButton.addEventListener('click', () => {
      const updatedData = {
        title: titleInput.value,
        content: contentInput.value
      };
      updatePost(post.id, updatedData);
    });
  
    updateForm.appendChild(titleInput);
    updateForm.appendChild(contentInput);
    updateForm.appendChild(submitButton);
  
    updateForm.dataset.postId = post.id; // Add data-postId attribute
  
    return updateForm;
}

// Function to send a POST request to the API to add a new post
function addPost() {
    // Retrieve the values from the input fields
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;
    var postAuthor = document.getElementById('post-author').value;

    // Use the Fetch API to send a POST request to the /posts endpoint
    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: postTitle, content: postContent, author: postAuthor })
    })
    .then(response => response.json())  // Parse the JSON data from the response
    .then(post => {
        console.log('Post added:', post);
        loadPosts(); // Reload the posts after adding a new one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;
    console.log(baseUrl)

    // Use the Fetch API to send a DELETE request to the specific post's endpoint
    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('Post deleted:', postId);
        loadPosts(); // Reload the posts after deleting one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a PUT request to the API to update a post
function updatePost(postId, updatedData) {
    const baseUrl = document.getElementById('api-base-url').value;
  
    fetch(baseUrl + '/posts/' + postId, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updatedData)
    })
    .then(response => {
      if (response.ok) {
        console.log('Post updated:', postId);
        loadPosts(); // Reload posts after successful update
      } else {
        console.error('Error updating post:', postId, response.status);
        // Handle error (e.g., display error message to user)
      }
    })
    .catch(error => {
      console.error('Network error:', error);
      // Handle network errors (e.g., display error message to user)
    });
}
  