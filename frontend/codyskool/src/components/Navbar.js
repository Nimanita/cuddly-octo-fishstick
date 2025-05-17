import React from 'react';

export default function Navbar({ user, onLoginClick, onLogoutClick }) {
  return (
    <nav className="bg-blue-500 text-white p-4 flex justify-between items-center">
      <div className="text-2xl font-bold">codyskool</div>
      <div>
        {user ? (
          <button onClick={onLogoutClick} className="mr-4">
            Logout
          </button>
        ) : (
          <button onClick={onLoginClick} className="mr-4">
            Login
          </button>
        )}
      </div>
    </nav>
  );
}
