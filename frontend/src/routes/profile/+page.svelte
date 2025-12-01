<svelte:head>
	<title>Profile</title>
	<meta name="description" content="User Profile" />
</svelte:head>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StudyConnect - Profile Settings</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #4361ee;
            --secondary: #3a0ca3;
            --accent: #7209b7;
            --light: #f8f9fa;
            --dark: #212529;
            --success: #4cc9f0;
            --warning: #f72585;
            --gray: #6c757d;
            --light-gray: #e9ecef;
            --facebook-blue: #1877f2;
            --facebook-gray: #f0f2f5;
            --facebook-dark-gray: #65676b;
            --facebook-border: #dddfe2;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background-color: var(--facebook-gray);
            color: var(--dark);
            line-height: 1.6;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            background: var(--facebook-blue);
            color: white;
        }
        
        .logo {
            font-size: 24px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .nav-links {
            display: flex;
            gap: 20px;
        }
        
        .nav-links a {
            text-decoration: none;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 500;
            transition: color 0.3s;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .nav-links a:hover, .nav-links a.active {
            color: white;
        }
        
        .profile-container {
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 0;
        }
        
        .profile-sidebar {
            background: white;
            border-right: 1px solid var(--facebook-border);
            height: 100%;
        }
        
        .profile-card {
            background: white;
            border-radius: 0;
            box-shadow: none;
            border-bottom: 1px solid var(--facebook-border);
        }
        
        .cover-photo {
            height: 120px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 0;
        }
        
        .profile-info {
            padding: 0 15px 15px;
            text-align: center;
            margin-top: -50px;
        }
        
        .profile-picture-container {
            position: relative;
            display: inline-block;
            margin-bottom: 10px;
        }
        
        .profile-picture {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            object-fit: cover;
            border: 4px solid white;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        .change-avatar-btn {
            position: absolute;
            bottom: 5px;
            right: 5px;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: var(--facebook-blue);
            color: white;
            border: 2px solid white;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 12px;
        }
        
        .avatar-options {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 15px;
            padding: 10px;
            background: var(--facebook-gray);
            border-radius: 8px;
        }
        
        .avatar-option {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            object-fit: cover;
            cursor: pointer;
            border: 2px solid transparent;
            transition: all 0.3s;
        }
        
        .avatar-option:hover, .avatar-option.selected {
            border-color: var(--facebook-blue);
        }
        
        .profile-name {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .profile-major {
            color: var(--facebook-dark-gray);
            margin-bottom: 10px;
            font-size: 14px;
        }
        
        .profile-university {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            color: var(--facebook-dark-gray);
            font-size: 14px;
        }
        
        .profile-stats {
            display: flex;
            justify-content: space-around;
            margin: 15px 0;
            padding: 15px 0;
            border-top: 1px solid var(--facebook-border);
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-value {
            font-size: 18px;
            font-weight: 600;
            color: var(--facebook-blue);
        }
        
        .stat-label {
            font-size: 14px;
            color: var(--facebook-dark-gray);
        }
        
        .sidebar-nav {
            padding: 15px 0;
        }
        
        .nav-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 15px;
            text-decoration: none;
            color: var(--dark);
            transition: background 0.2s;
            border-left: 3px solid transparent;
        }
        
        .nav-item:hover {
            background: var(--facebook-gray);
        }
        
        .nav-item.active {
            background: var(--facebook-gray);
            border-left-color: var(--facebook-blue);
            color: var(--facebook-blue);
            font-weight: 600;
        }
        
        .profile-content {
            padding: 20px;
            background: var(--facebook-gray);
        }
        
        .content-header {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        
        .content-header h2 {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 20px;
        }
        
        .tabs {
            display: flex;
            border-bottom: 1px solid var(--facebook-border);
        }
        
        .tab {
            padding: 12px 24px;
            cursor: pointer;
            font-weight: 500;
            color: var(--facebook-dark-gray);
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
        }
        
        .tab.active {
            color: var(--facebook-blue);
            border-bottom: 3px solid var(--facebook-blue);
        }
        
        .tab-content {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--dark);
        }
        
        .form-control {
            width: 100%;
            padding: 12px 15px;
            border: 1px solid var(--facebook-border);
            border-radius: 6px;
            font-size: 16px;
            transition: all 0.3s;
            background: white;
        }
        
        .form-control:focus {
            outline: none;
            border-color: var(--facebook-blue);
            box-shadow: 0 0 0 2px rgba(24, 119, 242, 0.2);
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .btn {
            padding: 12px 20px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-primary {
            background-color: var(--facebook-blue);
            color: white;
        }
        
        .btn-primary:hover {
            background-color: #166fe5;
        }
        
        .btn-outline {
            background-color: transparent;
            border: 1px solid var(--facebook-border);
            color: var(--facebook-dark-gray);
        }
        
        .btn-outline:hover {
            background-color: var(--facebook-gray);
        }
        
        .toggle-switch {
            position: relative;
            display: inline-block;
            width: 50px;
            height: 24px;
        }
        
        .toggle-switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 24px;
        }
        
        .slider:before {
            position: absolute;
            content: "";
            height: 16px;
            width: 16px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        
        input:checked + .slider {
            background-color: var(--facebook-blue);
        }
        
        input:checked + .slider:before {
            transform: translateX(26px);
        }
        
        .toggle-label {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding: 15px;
            background: var(--facebook-gray);
            border-radius: 8px;
        }
        
        .toggle-text {
            flex: 1;
        }
        
        .courses-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }
        
        .course-tag {
            background-color: var(--facebook-gray);
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 14px;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }
        
        .course-tag span {
            cursor: pointer;
            color: var(--facebook-dark-gray);
        }
        
        .course-tag span:hover {
            color: var(--warning);
        }
        
        .add-course {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        
        .add-course .form-control {
            flex: 1;
        }
        
        .save-status {
            padding: 10px 15px;
            border-radius: 6px;
            margin-top: 15px;
            display: none;
            align-items: center;
            gap: 10px;
        }
        
        .save-status.success {
            background-color: rgba(76, 201, 240, 0.2);
            color: var(--success);
            display: flex;
        }
        
        .save-status.error {
            background-color: rgba(247, 37, 133, 0.2);
            color: var(--warning);
            display: flex;
        }
        
        @media (max-width: 768px) {
            .profile-container {
                grid-template-columns: 1fr;
            }
            
            .form-row {
                grid-template-columns: 1fr;
            }
            
            .profile-sidebar {
                border-right: none;
                border-bottom: 1px solid var(--facebook-border);
            }
            
            .tabs {
                overflow-x: auto;
                white-space: nowrap;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">
                <i class="fas fa-users"></i>
                <span>StudyConnect</span>
            </div>
            <nav class="nav-links">
                <a href="/"><i class="fas fa-home"></i> Dashboard</a>
                <a href="/groups"><i class="fas fa-user-friends"></i> Groups</a>
                <a href="/messages"><i class="fas fa-comments"></i> Messages</a>
                <a href="/profile" class="active"><i class="fas fa-user"></i> Profile</a>
            </nav>
        </header>
        
        <div class="profile-container">
            <div class="profile-sidebar">
                <div class="profile-card">
                    <div class="cover-photo"></div>
                    <div class="profile-info">
                        <div class="profile-picture-container">
                            <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=300&q=80" alt="Profile" class="profile-picture" id="profilePicture">
                            <button class="change-avatar-btn" id="changeAvatarBtn" aria-label="Change profile picture">
                                <i class="fas fa-camera"></i>
                            </button>
                        </div>
                        
                        <div class="avatar-options" id="avatarOptions" style="display: none;">
                            <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=300&q=80" alt="Avatar 1" class="avatar-option" data-avatar="1">
                            <img src="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=300&q=80" alt="Avatar 2" class="avatar-option" data-avatar="2">
                            <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=300&q=80" alt="Avatar 3" class="avatar-option" data-avatar="3">
                        </div>
                        
                        <h2 class="profile-name" id="profileName">Alex Johnson</h2>
                        <p class="profile-major" id="profileMajor">Computer Science</p>
                        <div class="profile-university">
                            <i class="fas fa-university"></i>
                            <span id="profileUniversity">Stanford University</span>
                        </div>
                    </div>
                    
                    <div class="profile-stats">
                        <div class="stat">
                            <div class="stat-value">0</div>
                            <div class="stat-label">Study Groups</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">0</div>
                            <div class="stat-label">Connections</div>
                        </div>
                    </div>
                </div>
                
                <!-- Facebook-style navigation -->
                <div class="sidebar-nav">
                    <a href="/profile" class="nav-item active">
                        <i class="fas fa-user"></i>
                        <span>Profile</span>
                    </a>
                    <a href="/profile/photos" class="nav-item">
                        <i class="fas fa-photo-video"></i>
                        <span>Photos</span>
                    </a>
                    <a href="/profile/groups" class="nav-item">
                        <i class="fas fa-users"></i>
                        <span>Study Groups</span>
                    </a>
                    <a href="/profile/events" class="nav-item">
                        <i class="fas fa-calendar-alt"></i>
                        <span>Events</span>
                    </a>
                    <a href="/profile/courses" class="nav-item">
                        <i class="fas fa-book"></i>
                        <span>Courses</span>
                    </a>
                </div>
            </div>
            
            <!-- Main content area -->
            <div class="profile-content">
                <div class="content-header">
                    <h2>Profile Settings</h2>
                    <div class="tabs">
                        <div class="tab active" data-tab="personal">
                            <i class="fas fa-user"></i> Personal Info
                        </div>
                        <div class="tab" data-tab="academic">
                            <i class="fas fa-graduation-cap"></i> Academic Info
                        </div>
                        <div class="tab" data-tab="privacy">
                            <i class="fas fa-shield-alt"></i> Privacy
                        </div>
                    </div>
                </div>
                
                <!-- Personal Info Tab -->
                <div class="tab-content active" id="personal-tab">
                    <form id="profile-form">
                        <div class="form-row">
                            <div class="form-group">
                                <label for="firstName">First Name</label>
                                <input type="text" id="firstName" class="form-control" value="Alex" required>
                            </div>
                            <div class="form-group">
                                <label for="lastName">Last Name</label>
                                <input type="text" id="lastName" class="form-control" value="Johnson" required>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label for="email">Email Address</label>
                            <input type="email" id="email" class="form-control" value="alex.johnson@stanford.edu" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="bio">Bio</label>
                            <textarea id="bio" class="form-control" rows="4">Computer Science student interested in AI and machine learning. Looking for study partners for advanced algorithms course.</textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="interests">Interests</label>
                            <input type="text" id="interests" class="form-control" value="Machine Learning, Algorithms, Data Structures, Python">
                            <small>Separate interests with commas</small>
                        </div>
                        
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save"></i> Save Changes
                        </button>
                        
                        <div class="save-status success" id="personalSaveStatus">
                            <i class="fas fa-check-circle"></i>
                            <span>Your personal information has been updated successfully!</span>
                        </div>
                    </form>
                </div>
                
                <!-- Academic Info Tab -->
                <div class="tab-content" id="academic-tab">
                    <div class="form-group">
                        <label for="university">University</label>
                        <select id="university" class="form-control">
                            <option selected>Stanford University</option>
                            <option>Harvard University</option>
                            <option>MIT</option>
                            <option>WSU</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="major">Major</label>
                        <input type="text" id="major" class="form-control" value="Computer Science">
                    </div>
                    
                    <div class="form-group">
                        <label for="year">Academic Year</label>
                        <select id="year" class="form-control">
                            <option>Freshman</option>
                            <option>Sophomore</option>
                            <option selected>Junior</option>
                            <option>Senior</option>
                            <option>Graduate</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="newCourse">Current Courses</label>
                        <div class="courses-list" id="coursesList">
                            <div class="course-tag">CS229: Machine Learning <span>&times;</span></div>
                            <div class="course-tag">CS161: Algorithms <span>&times;</span></div>
                            <div class="course-tag">MATH101: Linear Algebra <span>&times;</span></div>
                        </div>
                        <div class="add-course">
                            <input type="text" class="form-control" placeholder="Add a course" id="newCourse">
                            <button type="button" class="btn btn-outline" id="addCourseBtn">
                                <i class="fas fa-plus"></i> Add
                            </button>
                        </div>
                    </div>
                    
                    <button class="btn btn-primary" id="saveAcademicBtn">
                        <i class="fas fa-save"></i> Save Academic Info
                    </button>
                    
                    <div class="save-status success" id="academicSaveStatus">
                        <i class="fas fa-check-circle"></i>
                        <span>Your academic information has been updated successfully!</span>
                    </div>
                </div>
                
                <!-- Privacy Tab -->
                <div class="tab-content" id="privacy-tab">
                    <div class="toggle-label">
                        <div class="toggle-text">
                            <strong>Profile Visibility</strong>
                            <p>Make your profile visible to other students</p>
                        </div>
                        <label class="toggle-switch">
                            <input type="checkbox" id="profileVisibility" checked>
                            <span class="slider"></span>
                        </label>
                    </div>
                    
                    <div class="toggle-label">
                        <div class="toggle-text">
                            <strong>Study Group Recommendations</strong>
                            <p>Allow us to suggest relevant study groups</p>
                        </div>
                        <label class="toggle-switch">
                            <input type="checkbox" id="groupRecommendations" checked>
                            <span class="slider"></span>
                        </label>
                    </div>
                    
                    <div class="toggle-label">
                        <div class="toggle-text">
                            <strong>Email Notifications</strong>
                            <p>Receive emails about new study groups and messages</p>
                        </div>
                        <label class="toggle-switch">
                            <input type="checkbox" id="emailNotifications" checked>
                            <span class="slider"></span>
                        </label>
                    </div>
                    
                    <div class="toggle-label">
                        <div class="toggle-text">
                            <strong>Canvas Integration</strong>
                            <p>Sync your courses from Canvas LMS</p>
                        </div>
                        <label class="toggle-switch">
                            <input type="checkbox" id="canvasIntegration">
                            <span class="slider"></span>
                        </label>
                    </div>
                    
                    <div style="margin-top: 30px;">
                        <button class="btn btn-primary" id="savePrivacyBtn">
                            <i class="fas fa-save"></i> Save Privacy Settings
                        </button>
                    </div>
                    
                    <div class="save-status success" id="privacySaveStatus">
                        <i class="fas fa-check-circle"></i>
                        <span>Your privacy settings have been updated successfully!</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Tab switching functionality
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                // Remove active class from all tabs and content
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                
                // Add active class to clicked tab and corresponding content
                tab.classList.add('active');
                document.getElementById(`${tab.dataset.tab}-tab`).classList.add('active');
            });
        });
        
        // Form submission
        document.getElementById('profile-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const firstName = document.getElementById('firstName').value;
            const lastName = document.getElementById('lastName').value;
            const email = document.getElementById('email').value;
            const bio = document.getElementById('bio').value;
            const interests = document.getElementById('interests').value;
            
            // Update profile sidebar in real-time
            document.getElementById('profileName').textContent = `${firstName} ${lastName}`;
            
            // Show save status
            const saveStatus = document.getElementById('personalSaveStatus');
            saveStatus.classList.add('success');
            saveStatus.style.display = 'flex';
            
            // Hide status after 3 seconds
            setTimeout(() => {
                saveStatus.style.display = 'none';
            }, 3000);
        });
        
        // Save academic info
        document.getElementById('saveAcademicBtn').addEventListener('click', function() {
            const university = document.getElementById('university').value;
            const major = document.getElementById('major').value;
            
            // Update profile sidebar in real-time
            document.getElementById('profileUniversity').textContent = university;
            document.getElementById('profileMajor').textContent = major;
            
            // Show save status
            const saveStatus = document.getElementById('academicSaveStatus');
            saveStatus.classList.add('success');
            saveStatus.style.display = 'flex';
            
            // Hide status after 3 seconds
            setTimeout(() => {
                saveStatus.style.display = 'none';
            }, 3000);
        });
        
        // Save privacy settings
        document.getElementById('savePrivacyBtn').addEventListener('click', function() {
            // Show save status
            const saveStatus = document.getElementById('privacySaveStatus');
            saveStatus.classList.add('success');
            saveStatus.style.display = 'flex';
            
            // Hide status after 3 seconds
            setTimeout(() => {
                saveStatus.style.display = 'none';
            }, 3000);
        });
        
        // Course tag removal
        document.querySelectorAll('.course-tag span').forEach(span => {
            span.addEventListener('click', function() {
                this.parentElement.remove();
            });
        });
        
        // Add course functionality
        document.getElementById('addCourseBtn').addEventListener('click', function() {
            const newCourseInput = document.getElementById('newCourse');
            const courseName = newCourseInput.value.trim();
            
            if (courseName) {
                const courseTag = document.createElement('div');
                courseTag.className = 'course-tag';
                courseTag.innerHTML = `${courseName} <span>&times;</span>`;
                
                // Add event listener to the remove button
                courseTag.querySelector('span').addEventListener('click', function() {
                    this.parentElement.remove();
                });
                
                document.getElementById('coursesList').appendChild(courseTag);
                newCourseInput.value = '';
            }
        });
        
        // Change avatar functionality
        document.getElementById('changeAvatarBtn').addEventListener('click', function() {
            const avatarOptions = document.getElementById('avatarOptions');
            avatarOptions.style.display = avatarOptions.style.display === 'none' ? 'flex' : 'none';
        });
        
        document.querySelectorAll('.avatar-option').forEach(avatar => {
            avatar.addEventListener('click', function() {
                // Set selected class
                document.querySelectorAll('.avatar-option').forEach(a => a.classList.remove('selected'));
                this.classList.add('selected');
                
                // Update profile picture
                document.getElementById('profilePicture').src = this.src;
                
                // Hide options after selection
                document.getElementById('avatarOptions').style.display = 'none';
            });
        });
    </script>
</body>
</html>