"""
COMPREHENSIVE FRONTEND DESIGN PROMPT FOR AI

Project: Social Media Platform with Real-time Messaging & Content Management

PROJECT OVERVIEW:
This is a full-featured social media platform similar to Reddit + WhatsApp built with FastAPI backend and PostgreSQL database. The backend has all the APIs ready and WebSocket support for real-time features.

KEY FEATURES TO IMPLEMENT IN FRONTEND:

1. AUTHENTICATION SYSTEM
   - User registration page with email, username, password
   - Login page with email and password
   - Session management and JWT token storage
   - Logout functionality
   - Profile verification status indicator
   - Password reset/forgot password flow

2. USER PROFILE SYSTEM
   - User profile page (own and others)
   - Edit profile functionality
   - Display user info: username, email, account creation date
   - User statistics: posts created, comments, followers count
   - Profile picture/avatar
   - User bio/description
   - Online/offline status indicator

3. POSTS & FEED SYSTEM
   - Create new post with title, content, optional image/file
   - Main feed showing all posts
   - Post display with:
     * Author name and avatar
     * Post title and content
     * Creation date and time
     * Like/upvote counter
     * Comment counter
     * Share button
   - Pagination for feed
   - Sort posts by: newest, most popular, trending
   - Search posts by keyword
   - Edit own posts
   - Delete own posts
   - Post detail view

4. VOTING SYSTEM
   - Upvote/downvote posts
   - Upvote/downvote comments
   - Show vote count on each post/comment
   - Visual indicator of user's vote (liked/disliked)
   - Vote counter updates in real-time

5. COMMENTS SYSTEM
   - View comments on posts
   - Add comments to posts
   - Reply to comments (nested comments)
   - Edit own comments
   - Delete own comments
   - Comment author info (name, avatar, timestamp)
   - Upvote/downvote comments
   - Pagination for long comment threads
   - Sort comments by newest/most popular

6. PRIVATE MESSAGING & REAL-TIME CHAT
   - Contact list showing all users
   - Start new conversation with any user
   - Real-time chat interface with WebSocket support
   - Message history display (scrollable)
   - Send/receive messages instantly
   - Show message timestamps
   - Unread message indicator
   - Message sender/recipient visual distinction
   - Online status indicator for contacts
   - Typing indicator (optional)
   - Search conversations
   - Delete conversations

7. FILE MANAGEMENT
   - Upload files (documents, images, videos)
   - File list/gallery view
   - File download functionality
   - File metadata display (name, size, upload date, uploader)
   - File preview (images, documents if possible)
   - Delete own files
   - Share files with other users

8. NOTIFICATIONS SYSTEM
   - Notification badge count
   - Notification center/dropdown
   - Notifications for:
     * New comments on posts
     * New messages
     * Post likes/votes
     * User follows
   - Mark notification as read
   - Clear notifications

9. MODERATION/REPORTING
   - Report post/comment functionality
   - Report form with reason selection
   - Report status indicator
   - Moderation dashboard (if user is moderator)
   - View reported content

10. RESPONSIVE DESIGN
    - Mobile-friendly layout
    - Tablet-friendly layout
    - Desktop layout
    - Dark mode / Light mode toggle
    - Adaptive navigation (hamburger menu on mobile)

11. USER INTERFACE COMPONENTS NEEDED
    - Navbar/Header with navigation, search, user menu, notifications
    - Sidebar for navigation (desktop)
    - Main content area
    - Cards for posts
    - Modals for forms (create post, compose message, etc)
    - Toast/alert notifications for user feedback
    - Loading spinners
    - Buttons with states (normal, hover, active, disabled)
    - Input fields with validation feedback
    - Avatars and user info widgets
    - Timestamp displays with relative time (e.g., "2 hours ago")
    - Like/vote button with counter
    - Comments section
    - Chat message bubbles (left/right)

12. NAVIGATION STRUCTURE
    - Home/Feed page
    - Profile page (my profile + view other profiles)
    - Messages/Chat page
    - Notifications page
    - Create post page
    - Post detail page
    - User search/discovery page
    - Settings page

13. BACKEND ENDPOINTS AVAILABLE (All ready to use):
    - Auth: /auth/register, /auth/login, /auth/logout
    - Users: /users/me, /users/{id}, /users/by-username/{username}
    - Posts: /posts (GET/POST), /posts/{id} (GET/PUT/DELETE)
    - Comments: /comments, /comments/{id}
    - Votes: /votes/posts, /votes/comments
    - Messages: /messages/, /messages/conversation/{user_id}
    - WebSocket: /ws/chat/{user_id}?token={token}
    - Files: /files (GET/POST), /files/{id}
    - Reports: /reports, /reports/{id}

14. DESIGN REQUIREMENTS
    - Modern, clean aesthetic
    - Intuitive user experience
    - Consistent color scheme (primary, secondary, accent colors)
    - Proper spacing and typography
    - Accessible design (WCAG 2.1 AA compliant)
    - Micro-interactions and smooth transitions
    - Loading states for async operations
    - Error handling and user feedback
    - Form validation with helpful error messages

15. PERFORMANCE CONSIDERATIONS
    - Lazy loading for feeds and comments
    - Pagination instead of infinite scroll (or implement both)
    - Image optimization/lazy loading
    - Debouncing for search and input fields
    - Efficient state management
    - Caching where appropriate

TECHNICAL REQUIREMENTS:
- Tech Stack: React.js (or Vue/Angular - your choice)
- State Management: Redux/Zustand/Pinia (your choice)
- Styling: Tailwind CSS or CSS-in-JS
- HTTP Client: Axios or Fetch API
- WebSocket: Socket.io or native WebSocket API
- UI Components Library: Material-UI, Chakra UI, or shadcn/ui (optional)
- Package Manager: npm or yarn
- Build Tool: Vite or Create React App

API BASE URL: http://localhost:8000

DELIVERABLES:
1. Complete responsive frontend application
2. All pages and components as described above
3. Real-time WebSocket chat integration
4. Proper error handling and loading states
5. User authentication flow
6. Dark/Light mode toggle
7. Mobile responsive design
8. All features fully functional and integrated with backend APIs
9. Clean, maintainable code with proper folder structure
10. Environment configuration file for API endpoints

Please create a complete, production-ready frontend application that implements all the above features with excellent UX/UI design.
"""
