import DailySadhanaReport from "./features/sadhana-reports/pages/DailySadhanaReport";
import { useState, useEffect } from "react";
import AuthPage from "./features/auth/AuthPage";
import {
  authAPI,
  getToken,
  getStoredUser,
  clearAuthData,
} from "./services/api";
import {
  LayoutDashboard,
  ClipboardList,
  History,
  TrendingUp,
  UserRound,
  Settings,
  Bell,
  Search,
  Menu,
  X,
  Sun,
  BookOpen,
  Heart,
  Clock,
  Moon,
  Flame,
  Headphones,
  HandHeart,
  CalendarDays,
  ChevronRight,
  CircleCheck,
  Flower2,
  LogOut,
} from "lucide-react";

import "./App.css";

const navigation = [
  { name: "Dashboard", icon: LayoutDashboard },
  { name: "Daily Sadhana Report", icon: ClipboardList },
  { name: "Report History", icon: History },
  { name: "My Progress", icon: TrendingUp },
  { name: "My Profile", icon: UserRound },
];

function App() {
  const [activePage, setActivePage] = useState("Dashboard");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const [user, setUser] = useState(getStoredUser());
  const [checkingAuth, setCheckingAuth] = useState(true);

  // Check whether the user is already logged in
  useEffect(() => {
    let mounted = true;

    const verifyAuth = async () => {
      if (!getToken()) {
        if (mounted) setCheckingAuth(false);
        return;
      }

      try {
        const currentUser = await authAPI.me();

        if (mounted) {
          setUser(currentUser);
        }
      } catch {
        clearAuthData();

        if (mounted) {
          setUser(null);
        }
      } finally {
        if (mounted) {
          setCheckingAuth(false);
        }
      }
    };

    verifyAuth();

    return () => {
      mounted = false;
    };
  }, []);

  // Called after successful login or registration
  const handleAuthenticated = (authenticatedUser) => {
    setUser(authenticatedUser);
    setActivePage("Dashboard");
  };

  // Logout the current user
  const handleLogout = async () => {
    try {
      await authAPI.logout();
    } catch {
      clearAuthData();
    } finally {
      setUser(null);
      setActivePage("Dashboard");
      setSidebarOpen(false);
    }
  };

  // Show loading while checking login
  if (checkingAuth) {
    return (
      <div style={{ padding: "40px", textAlign: "center" }}>
        Loading NityaSadhana...
      </div>
    );
  }

  // Show login/register if the user is not logged in
  if (!user) {
    return <AuthPage onAuthenticated={handleAuthenticated} />;
  }

  const today = new Date().toLocaleDateString("en-IN", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <div className="app-container">
      {sidebarOpen && (
        <div
          className="sidebar-overlay"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <aside className={`sidebar ${sidebarOpen ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-icon">
            <Flower2 size={27} />
          </div>

          <div>
            <h2>NityaSadhana</h2>
            <p>A Daily Journey of Devotion</p>
          </div>

          <button
            className="close-sidebar"
            onClick={() => setSidebarOpen(false)}
          >
            <X size={20} />
          </button>
        </div>

        <div className="nav-heading">MAIN MENU</div>

        <nav className="navigation">
          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.name}
                className={`nav-item ${
                  activePage === item.name ? "active" : ""
                }`}
                onClick={() => {
                  setActivePage(item.name);
                  setSidebarOpen(false);
                }}
              >
                <Icon size={19} />
                <span>{item.name}</span>
              </button>
            );
          })}
        </nav>

        <div className="nav-heading settings-heading">PREFERENCES</div>

        <button
          className={`nav-item ${
            activePage === "Settings" ? "active" : ""
          }`}
          onClick={() => {
            setActivePage("Settings");
            setSidebarOpen(false);
          }}
        >
          <Settings size={19} />
          <span>Settings</span>
        </button>

        <div className="sidebar-bottom">
          <div className="devotion-card">
            <div className="devotion-flower">
              <Flower2 size={25} />
            </div>
            <h3>Keep growing in devotion</h3>
            <p>
              Small daily efforts bring us closer to Krishna.
            </p>
            <span>Hare Krishna! 🙏</span>
          </div>

          <div className="user-profile">
            <div className="avatar">D</div>
            <div className="user-details">
              <strong>Devotee</strong>
              <span>Devotee Account</span>
            </div>
            <LogOut size={17} className="logout-icon" />
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="topbar-left">
            <button
              className="menu-button"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu size={23} />
            </button>

            <div>
              <span className="breadcrumb">NityaSadhana</span>
              <span className="breadcrumb-separator"> / </span>
              <span className="breadcrumb-current">{activePage}</span>
            </div>
          </div>

          <div className="topbar-right">
            <div className="today-date">
              <CalendarDays size={17} />
              <span>{today}</span>
            </div>

            <button className="notification-button" aria-label="Notifications">
              <Bell size={20} />
              <span className="notification-dot"></span>
            </button>

            <div className="top-avatar">
  {(user?.name || user?.email || "D").charAt(0).toUpperCase()}
</div>
          </div>
        </header>

        {activePage === "Daily Sadhana Report" ? (
 <DailySadhanaReport onBack={() => setActivePage("Dashboard")} />
) : activePage === "Dashboard" ? (
          <div className="dashboard">
            <section className="welcome-section">
              <div>
                <span className="welcome-label">
                  <Sun size={17} />
                  YOUR SPIRITUAL JOURNEY
                </span>

                <h1>Hare Krishna! 🙏</h1>

                <p>
                  Welcome to your daily sadhana space. Every day is
                  another opportunity to serve and remember Krishna.
                </p>
              </div>

              <div className="welcome-decoration">
                <Flower2 size={105} strokeWidth={0.8} />
              </div>
            </section>

            <section className="section-heading">
              <div>
                <h2>Today's Overview</h2>
                <p>Your daily spiritual activities at a glance.</p>
              </div>

              <span className="status-badge">
                <span className="status-dot"></span>
                Report not submitted
              </span>
            </section>

            <section className="stats-grid">
              <StatCard
                icon={Flame}
                title="Japa Rounds"
                value="0"
                description="Rounds completed today"
                color="saffron"
              />

              <StatCard
                icon={BookOpen}
                title="Reading"
                value="0 min"
                description="Time spent reading"
                color="green"
              />

              <StatCard
                icon={Headphones}
                title="Hearing"
                value="0 min"
                description="Time spent hearing"
                color="gold"
              />

              <StatCard
                icon={Clock}
                title="Total Sadhana"
                value="0 min"
                description="Recorded activity time"
                color="brown"
              />
            </section>

            <section className="dashboard-grid">
              <div className="panel daily-report-panel">
                <div className="panel-heading">
                  <div>
                    <h2>Daily Sadhana Report</h2>
                    <p>Record your devotional activities.</p>
                  </div>
                  <div className="panel-icon">
                    <ClipboardList size={21} />
                  </div>
                </div>

                <div className="report-empty">
                  <div className="empty-icon">
                    <Flower2 size={36} />
                  </div>
                  <h3>Your report is waiting</h3>
                  <p>
                    You haven't submitted today's sadhana report yet.
                    Take a moment to record your activities.
                  </p>

                  <button
                    className="primary-button"
                    onClick={() =>
                      setActivePage("Daily Sadhana Report")
                    }
                  >
                    Fill Daily Report
                    <ChevronRight size={18} />
                  </button>
                </div>
              </div>

              <div className="panel activity-panel">
                <div className="panel-heading">
                  <div>
                    <h2>Daily Activities</h2>
                    <p>Your sadhana categories.</p>
                  </div>
                  <div className="panel-icon">
                    <Heart size={21} />
                  </div>
                </div>

                <ActivityRow
                  icon={Flame}
                  title="Japa"
                  subtitle="Hare Krishna Mahamantra"
                  value="Not recorded"
                />

                <ActivityRow
                  icon={BookOpen}
                  title="Reading (Paṭhanam)"
                  subtitle="Spiritual books"
                  value="Not recorded"
                />

                <ActivityRow
                  icon={Headphones}
                  title="Hearing (Śravaṇam)"
                  subtitle="Lectures and Krishna katha"
                  value="Not recorded"
                />

                <ActivityRow
                  icon={HandHeart}
                  title="Seva"
                  subtitle="Devotional service"
                  value="Not recorded"
                />

                <ActivityRow
                  icon={Sun}
                  title="Arati"
                  subtitle="Arati attendance"
                  value="Not recorded"
                />

                <ActivityRow
                  icon={Moon}
                  title="Sleep & Wake"
                  subtitle="Daily routine"
                  value="Not recorded"
                  last
                />
              </div>
            </section>

            <section className="bottom-grid">
              <div className="panel progress-panel">
                <div className="panel-heading">
                  <div>
                    <h2>Weekly Consistency</h2>
                    <p>Your report submission progress.</p>
                  </div>
                  <TrendingUp size={21} className="heading-icon" />
                </div>

                <div className="weekly-days">
                  {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map(
                    (day) => (
                      <div className="day-item" key={day}>
                        <div className="day-circle">
                          <span>–</span>
                        </div>
                        <span>{day}</span>
                      </div>
                    )
                  )}
                </div>

                <p className="weekly-note">
                  Your weekly progress will appear here after reports
                  are recorded.
                </p>
              </div>

              <div className="panel quote-panel">
                <div className="quote-symbol">“</div>
                <p>
                  Always remember Krishna, and never forget Him.
                </p>
                <span>Śrīla Prabhupāda's teachings</span>
                <div className="quote-flower">
                  <Flower2 size={48} />
                </div>
              </div>
            </section>

            <footer className="footer">
              <span>© 2026 NityaSadhana</span>
              <span>Made with devotion ❤️</span>
            </footer>
          </div>
        ) : (
          <div className="placeholder-page">
            <div className="placeholder-icon">
              <CircleCheck size={38} />
            </div>
            <h1>{activePage}</h1>
            <p>
              This section will be developed in the next stage of
              NityaSadhana.
            </p>
            <button
              className="primary-button"
              onClick={() => setActivePage("Dashboard")}
            >
              Return to Dashboard
              <ChevronRight size={18} />
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

function StatCard({ icon: Icon, title, value, description, color }) {
  return (
    <div className="stat-card">
      <div className={`stat-icon ${color}`}>
        <Icon size={22} />
      </div>
      <span className="stat-title">{title}</span>
      <h2>{value}</h2>
      <p>{description}</p>
    </div>
  );
}

function ActivityRow({ icon: Icon, title, subtitle, value, last }) {
  return (
    <div className={`activity-row ${last ? "last" : ""}`}>
      <div className="activity-icon">
        <Icon size={19} />
      </div>
      <div className="activity-details">
        <strong>{title}</strong>
        <span>{subtitle}</span>
      </div>
      <span className="activity-value">{value}</span>
    </div>
  );
}

export default App;
