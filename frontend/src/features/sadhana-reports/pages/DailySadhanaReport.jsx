import { reportAPI } from "../../../services/api";
import { useEffect, useMemo, useState } from "react";
import {
  ArrowLeft,
  BookOpen,
  Clock,
  Flame,
  Headphones,
  Heart,
  Moon,
  Sun,
  HandHeart,
  Video,
  Save,
  Eye,
  Send,
  Edit3,
  CheckCircle2,
  Copy,
  Flower2,
  Lock,
} from "lucide-react";

import "../styles/DailySadhanaReport.css";

const today = (() => {
  const d = new Date();
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
})();

const initialData = {
  wakeTime: "",
  sleepTime: "",
  japaRounds: "",
  japaDuration: "",
  japaStart: "",
  japaEnd: "",
  japaQuality: "",
  readingType: "",
  readingBook: "",
  readingDuration: "",
  hearingType: "",
  hearingTopic: "",
  hearingSpeaker: "",
  hearingDuration: "",
  hearingLink: "",
  sevaDetails: "",
  sevaDuration: "",
  arati: "",
  fourPrinciples: "",
  lectureTopic: "",
  lectureSpeaker: "",
  lectureDuration: "",
  lectureLink: "",
};

function getDuration(start, end) {
  if (!start || !end) return 0;

  const [sh, sm] = start.split(":").map(Number);
  const [eh, em] = end.split(":").map(Number);

  let difference = eh * 60 + em - (sh * 60 + sm);

  if (difference < 0) difference += 1440;

  return difference;
}

function formatMinutes(value) {
  const hours = Math.floor(value / 60);
  const minutes = value % 60;

  if (hours && minutes) return `${hours} hr ${minutes} min`;
  if (hours) return `${hours} hr`;
  return `${minutes} min`;
}

function getSleepDuration(wake, sleep) {
  return getDuration(sleep, wake);
}

function Section({ icon: Icon, title, subtitle, children, number }) {
  return (
    <section className="report-section">
      <div className="report-section-heading">
        <div className="report-section-icon">
          <Icon size={21} />
        </div>
        <div className="report-section-title">
          <div>
            <span className="section-number">SECTION {number}</span>
            <h3>{title}</h3>
          </div>
          <p>{subtitle}</p>
        </div>
      </div>
      <div className="report-section-body">{children}</div>
    </section>
  );
}

function Field({ label, children, full = false, hint }) {
  return (
    <div className={`report-field ${full ? "field-full" : ""}`}>
      <label>{label}</label>
      {children}
      {hint && <small>{hint}</small>}
    </div>
  );
}

function DurationField({ label, name, value, onChange }) {
  return (
    <Field label={label}>
      <div className="duration-input">
        <Clock size={17} />
        <input
          type="number"
          min="0"
          max="1440"
          placeholder="Minutes"
          value={value}
          onChange={(e) => onChange(name, e.target.value)}
        />
        <span>min</span>
      </div>
    </Field>
  );
}

export default function DailySadhanaReport({ onBack }) {
  const [data, setData] = useState(initialData);
  const [status, setStatus] = useState("New");
  const [submittedAt, setSubmittedAt] = useState(null);
  const [showPreview, setShowPreview] = useState(false);
  const [message, setMessage] = useState("");
  const [editingSubmitted, setEditingSubmitted] = useState(false);

  

  useEffect(() => {
  let active = true;

  const loadTodayReport = async () => {
    try {
      const report = await reportAPI.today();

      if (!active) return;

      setData({
        ...initialData,
        ...(report.report_data || {}),
      });

      setStatus(report.status || "Draft");
      setSubmittedAt(
        report.submitted_at
          ? new Date(report.submitted_at).getTime()
          : null
      );
    } catch (error) {
      if (!active) return;

      if (error.message.toLowerCase().includes("not found")) {
        setStatus("New");
        setSubmittedAt(null);
      } else {
        setMessage(`Unable to load today's report: ${error.message}`);
      }
    }
  };

  loadTodayReport();

  return () => {
    active = false;
  };
}, []);

  const isLocked =
    status === "Submitted" &&
    submittedAt &&
    Date.now() - submittedAt >= 24 * 60 * 60 * 1000;

  const isReadOnly = status === "Submitted" && !editingSubmitted;
  const canEdit = status === "Submitted" && !isLocked;

  const updateField = (name, value) => {
    setData((previous) => ({ ...previous, [name]: value }));
  };

  const totals = useMemo(() => {
    const japa = Number(data.japaDuration) || 0;
    const reading = Number(data.readingDuration) || 0;
    const hearing = Number(data.hearingDuration) || 0;
    const seva = Number(data.sevaDuration) || 0;
    const lectures = Number(data.lectureDuration) || 0;

    return {
      japa,
      reading,
      hearing,
      seva,
      lectures,
      total: japa + reading + hearing + seva + lectures,
      sleep: getSleepDuration(data.wakeTime, data.sleepTime),
    };
  }, [data]);

  const saveReport = async (nextStatus) => {
  try {
    const report =
      nextStatus === "Submitted"
        ? await reportAPI.submit(today, data)
        : await reportAPI.save(today, data);

    setStatus(report.status);

    setSubmittedAt(
      report.submitted_at
        ? new Date(report.submitted_at).getTime()
        : null
    );

    setEditingSubmitted(false);

    return report;
  } catch (error) {
    setMessage(`Error: ${error.message}`);
    return null;
  }
};

const handleDraft = async () => {
  const report = await saveReport("Draft");

  if (report) {
    setMessage("Draft saved successfully to the database.");
  }
};

  const handlePreview = () => {
    
    setShowPreview(true);
  };

  const handleEdit = () => {
  if (isLocked) return;
  setEditingSubmitted(true);
  setShowPreview(false);
};

  const handleSubmit = async () => {
  const confirmed = window.confirm(
    "Are you sure you want to submit today's Sadhana Report? You can edit it within 24 hours."
  );

  if (!confirmed) return;

  const report = await saveReport("Submitted");

  if (report) {
    setShowPreview(false);
    setMessage("Your report has been submitted successfully.");
  }
};

  const handleCopyPrevious = async () => {
  try {
    const previousReport = await reportAPI.previous();

    setData({
      ...initialData,
      ...(previousReport.report_data || {}),
    });

    setShowPreview(false);

    setMessage(
      "Previous day's report copied. Please review today's details and save."
    );
  } catch (error) {
    setMessage(
      error.message.toLowerCase().includes("not found")
        ? "No previous day's report found."
        : `Unable to copy previous report: ${error.message}`
    );
  }
};

  const fieldDisabled = isLocked || (isReadOnly && !showPreview);

  const renderValue = (value) => value || "Not recorded";

  const previewRows = [
    ["Wake-up time", data.wakeTime],
    ["Sleeping time", data.sleepTime],
    ["Japa rounds", data.japaRounds],
    ["Japa duration", data.japaDuration ? `${data.japaDuration} min` : ""],
    ["Japa quality", data.japaQuality],
    ["Reading type", data.readingType],
    ["Reading book", data.readingBook],
    ["Reading duration", data.readingDuration ? `${data.readingDuration} min` : ""],
    ["Hearing type", data.hearingType],
    ["Hearing topic", data.hearingTopic],
    ["Hearing speaker", data.hearingSpeaker],
    ["Hearing duration", data.hearingDuration ? `${data.hearingDuration} min` : ""],
    ["Seva details", data.sevaDetails],
    ["Seva duration", data.sevaDuration ? `${data.sevaDuration} min` : ""],
    ["Arati attendance", data.arati],
    ["Four regulative principles", data.fourPrinciples],
    ["Lecture topic", data.lectureTopic],
    ["Lecture speaker", data.lectureSpeaker],
    ["Lecture duration", data.lectureDuration ? `${data.lectureDuration} min` : ""],
  ];

  return (
    <div className="daily-report-page">
      <div className="report-page-top">
        <button
  className="back-dashboard"
  onClick={onBack}
>
  <ArrowLeft size={17} />
  Back
</button>

        <div className="report-page-date">
          <CalendarLabel />
        </div>
      </div>

      <div className="report-welcome">
        <div>
          <span className="report-eyebrow">
            <Flower2 size={15} /> DAILY DEVOTIONAL JOURNEY
          </span>
          <h1>Daily Sadhana Report</h1>
          <p>
            Record your daily devotional activities with sincerity and
            gratitude.
          </p>
        </div>
        <div className="report-welcome-flower">
          <Flower2 size={75} />
        </div>
      </div>

      <div className="report-status-bar">
        <div>
          <span className="status-label">REPORT STATUS</span>
          <strong className={`report-status ${status.toLowerCase()}`}>
            {isLocked ? "Locked" : status}
          </strong>
        </div>

        <button className="copy-report-button" onClick={handleCopyPrevious}>
          <Copy size={16} />
          Copy Previous Day
        </button>
      </div>

      {message && <div className="report-message">{message}</div>}

      {isLocked && (
        <div className="locked-message">
          <Lock size={19} />
          This report is locked because the 24-hour editing period has ended.
        </div>
      )}

      {showPreview ? (
        <div className="report-form-card preview-card">
          <div className="form-card-heading">
            <div>
              <span className="section-number">REPORT PREVIEW</span>
              <h2>Review Your Sadhana</h2>
              <p>Please check your entries before final submission.</p>
            </div>
            <Eye size={24} />
          </div>

          <div className="preview-list">
            {previewRows.map(([label, value]) => (
              <div className="preview-row" key={label}>
                <span>{label}</span>
                <strong>{renderValue(value)}</strong>
              </div>
            ))}
          </div>

          <div className="preview-total">
            <span>Total recorded activity</span>
            <strong>{formatMinutes(totals.total)}</strong>
          </div>

          <div className="form-actions">
            {!isLocked && (
  <button
    type="button"
    onClick={handleEdit}
  >
    Edit Report
  </button>
)}
            {!isLocked && (
              <button className="submit-button" onClick={handleSubmit}>
                <Send size={17} />
                Confirm & Submit
              </button>
            )}
          </div>
        </div>
      ) : (
        <div className="report-form-card">
          <div className="form-card-heading">
            <div>
              <span className="section-number">YOUR DAILY RECORD</span>
              <h2>Today's Activities</h2>
              <p>Fill in the details of your devotional practice.</p>
            </div>
            <span className="required-note">* Required fields where marked</span>
          </div>

          <fieldset disabled={fieldDisabled} className="report-fieldset">
            <Section
              number="01"
              icon={Sun}
              title="Wake-up & Sleep"
              subtitle="Maintain a balanced daily routine."
            >
              <div className="report-fields-grid">
                <Field label="Wake-up time">
                  <input
                    type="time"
                    value={data.wakeTime}
                    onChange={(e) => updateField("wakeTime", e.target.value)}
                  />
                </Field>

                <Field label="Sleeping time">
                  <input
                    type="time"
                    value={data.sleepTime}
                    onChange={(e) => updateField("sleepTime", e.target.value)}
                  />
                </Field>

                <Field label="Calculated sleep duration">
                  <div className="calculated-value">
                    <Moon size={17} />
                    {data.wakeTime && data.sleepTime
                      ? formatMinutes(totals.sleep)
                      : "Enter both times"}
                  </div>
                </Field>
              </div>
            </Section>

            <Section
              number="02"
              icon={Flame}
              title="Japa"
              subtitle="Hare Krishna Mahamantra chanting."
            >
              <div className="report-fields-grid">
                <Field label="Number of rounds">
                  <input
                    type="number"
                    min="0"
                    max="64"
                    placeholder="Enter rounds"
                    value={data.japaRounds}
                    onChange={(e) => updateField("japaRounds", e.target.value)}
                  />
                </Field>

                <DurationField
                  label="Total japa duration"
                  name="japaDuration"
                  value={data.japaDuration}
                  onChange={updateField}
                />

                <Field label="Japa start time">
                  <input
                    type="time"
                    value={data.japaStart}
                    onChange={(e) => updateField("japaStart", e.target.value)}
                  />
                </Field>

                <Field label="Japa end time">
                  <input
                    type="time"
                    value={data.japaEnd}
                    onChange={(e) => updateField("japaEnd", e.target.value)}
                  />
                </Field>

                <Field label="Japa quality" full>
                  <select
                    value={data.japaQuality}
                    onChange={(e) => updateField("japaQuality", e.target.value)}
                  >
                    <option value="">Select quality</option>
                    <option>Very attentive</option>
                    <option>Attentive</option>
                    <option>Average</option>
                    <option>Distracted</option>
                  </select>
                </Field>
              </div>
            </Section>

            <Section
              number="03"
              icon={BookOpen}
              title="Reading (Paṭhanam)"
              subtitle="Time spent reading spiritual books."
            >
              <div className="report-fields-grid">
                <Field label="Reading type">
                  <select
                    value={data.readingType}
                    onChange={(e) => updateField("readingType", e.target.value)}
                  >
                    <option value="">Select reading type</option>
                    <option>Śrīmad-Bhāgavatam</option>
                    <option>Bhagavad-gītā</option>
                    <option>Śrī Caitanya-caritāmṛta</option>
                    <option>Other Prabhupāda books</option>
                    <option>Other devotional reading</option>
                  </select>
                </Field>

                <Field label="Book / Chapter">
                  <input
                    placeholder="Enter book or chapter name"
                    value={data.readingBook}
                    onChange={(e) => updateField("readingBook", e.target.value)}
                  />
                </Field>

                <DurationField
                  label="Reading duration"
                  name="readingDuration"
                  value={data.readingDuration}
                  onChange={updateField}
                />
              </div>
            </Section>

            <Section
              number="04"
              icon={Headphones}
              title="Hearing (Śravaṇam)"
              subtitle="Hearing Krishna katha, lectures and devotional classes."
            >
              <div className="report-fields-grid">
                <Field label="Hearing type">
                  <select
                    value={data.hearingType}
                    onChange={(e) => updateField("hearingType", e.target.value)}
                  >
                    <option value="">Select hearing type</option>
                    <option>Śrīmad-Bhāgavatam class</option>
                    <option>Bhagavad-gītā class</option>
                    <option>Hari-katha</option>
                    <option>Bhajan / Kirtan</option>
                    <option>Other devotional hearing</option>
                  </select>
                </Field>

                <Field label="Topic">
                  <input
                    placeholder="Enter hearing topic"
                    value={data.hearingTopic}
                    onChange={(e) => updateField("hearingTopic", e.target.value)}
                  />
                </Field>

                <Field label="Speaker">
                  <input
                    placeholder="Enter speaker name"
                    value={data.hearingSpeaker}
                    onChange={(e) => updateField("hearingSpeaker", e.target.value)}
                  />
                </Field>

                <DurationField
                  label="Hearing duration"
                  name="hearingDuration"
                  value={data.hearingDuration}
                  onChange={updateField}
                />

                <Field label="Source / Link (optional)" full>
                  <input
                    type="url"
                    placeholder="https://..."
                    value={data.hearingLink}
                    onChange={(e) => updateField("hearingLink", e.target.value)}
                  />
                </Field>
              </div>
            </Section>

            <Section
              number="05"
              icon={HandHeart}
              title="Seva (Devotional Service)"
              subtitle="Record your devotional service for the day."
            >
              <div className="report-fields-grid">
                <Field label="Seva details" full>
                  <textarea
                    rows="3"
                    placeholder="Describe the seva you performed..."
                    value={data.sevaDetails}
                    onChange={(e) => updateField("sevaDetails", e.target.value)}
                  />
                </Field>

                <DurationField
                  label="Seva duration"
                  name="sevaDuration"
                  value={data.sevaDuration}
                  onChange={updateField}
                />
              </div>
            </Section>

            <Section
              number="06"
              icon={Heart}
              title="Arati Attendance"
              subtitle="Record your participation in arati."
            >
              <div className="report-fields-grid">
                <Field label="Did you attend arati?" full>
                  <select
                    value={data.arati}
                    onChange={(e) => updateField("arati", e.target.value)}
                  >
                    <option value="">Select an option</option>
                    <option>Maṅgala-ārati</option>
                    <option>Darshan-ārati</option>
                    <option>Both</option>
                    <option>Other arati</option>
                    <option>Not attended</option>
                  </select>
                </Field>
              </div>
            </Section>

            <Section
              number="07"
              icon={CheckCircle2}
              title="Four Regulative Principles"
              subtitle="A combined daily self-check."
            >
              <Field label="Did you follow all four regulative principles today?" full>
                <div className="principle-options">
                  <label>
                    <input
                      type="radio"
                      name="principles"
                      value="Yes"
                      checked={data.fourPrinciples === "Yes"}
                      onChange={(e) =>
                        updateField("fourPrinciples", e.target.value)
                      }
                    />
                    <span>Yes, I followed all four.</span>
                  </label>

                  <label>
                    <input
                      type="radio"
                      name="principles"
                      value="No"
                      checked={data.fourPrinciples === "No"}
                      onChange={(e) =>
                        updateField("fourPrinciples", e.target.value)
                      }
                    />
                    <span>No</span>
                  </label>
                </div>
              </Field>
            </Section>

            <Section
              number="08"
              icon={Video}
              title="Lectures"
              subtitle="Record lectures attended or watched."
            >
              <div className="report-fields-grid">
                <Field label="Lecture topic">
                  <input
                    placeholder="Enter lecture topic"
                    value={data.lectureTopic}
                    onChange={(e) => updateField("lectureTopic", e.target.value)}
                  />
                </Field>

                <Field label="Speaker">
                  <input
                    placeholder="Enter speaker name"
                    value={data.lectureSpeaker}
                    onChange={(e) =>
                      updateField("lectureSpeaker", e.target.value)
                    }
                  />
                </Field>

                <DurationField
                  label="Lecture duration"
                  name="lectureDuration"
                  value={data.lectureDuration}
                  onChange={updateField}
                />

                <Field label="Lecture link (optional)">
                  <input
                    type="url"
                    placeholder="https://..."
                    value={data.lectureLink}
                    onChange={(e) => updateField("lectureLink", e.target.value)}
                  />
                </Field>
              </div>
            </Section>
          </fieldset>

          <div className="activity-summary">
            <div className="summary-heading">
              <Clock size={20} />
              <div>
                <h3>Activity Summary</h3>
                <p>Automatically calculated from your entries.</p>
              </div>
            </div>

            <div className="summary-grid">
              <div>
                <span>Japa</span>
                <strong>{formatMinutes(totals.japa)}</strong>
              </div>
              <div>
                <span>Reading</span>
                <strong>{formatMinutes(totals.reading)}</strong>
              </div>
              <div>
                <span>Hearing</span>
                <strong>{formatMinutes(totals.hearing)}</strong>
              </div>
              <div>
                <span>Seva</span>
                <strong>{formatMinutes(totals.seva)}</strong>
              </div>
              <div>
                <span>Lectures</span>
                <strong>{formatMinutes(totals.lectures)}</strong>
              </div>
            </div>

            <div className="summary-total">
              <span>Total devotional activity time</span>
              <strong>{formatMinutes(totals.total)}</strong>
            </div>
          </div>

          <div className="form-actions">
  {!isLocked && !isReadOnly && (
    <>
      <button className="secondary-button" onClick={handleDraft}>
        <Save size={17} />
        Save Draft
      </button>

      <button className="submit-button" onClick={handlePreview}>
        <Eye size={17} />
        Preview Report
      </button>
    </>
  )}

  {isReadOnly && canEdit && !isLocked && (
    <button
      className="secondary-button"
      type="button"
      onClick={handleEdit}
    >
      <Edit3 size={17} />
      Edit Report
    </button>
  )}
</div>
        </div>
      )}

      <div className="report-footer">
        <Flower2 size={17} />
        <span>Every sincere effort is an offering to Krishna.</span>
      </div>
    </div>
  );
}

function CalendarLabel() {
  const formatted = new Date().toLocaleDateString("en-IN", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <span>
      <Clock size={16} />
      {formatted}
    </span>
  );
}
