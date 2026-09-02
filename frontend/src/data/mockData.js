/* ==========================================================================
   MOCK DATA
   Everything here is fake/placeholder data standing in for a real backend.
   When the backend team's APIs are ready, this is the only file that needs
   to be replaced with real fetch() calls.
   ========================================================================== */

// ---- Mock login credentials -------------------------------------------
// In the real system this would be a call to an auth API.
export const MOCK_CREDENTIALS = {
  username: 'officer1',
  password: 'authenova123',
};

export function mockLogin(username, password) {
  if (
    username === MOCK_CREDENTIALS.username &&
    password === MOCK_CREDENTIALS.password
  ) {
    return { success: true };
  }
  return { success: false, message: 'Incorrect username or password.' };
}

// ---- Pipeline stages shown on the progress screen ----------------------
export const PIPELINE_STAGES = [
  { key: 'reading', label: 'Reading Document' },
  { key: 'validating', label: 'Validating Fields' },
  { key: 'tampering', label: 'Checking for Tampering' },
  { key: 'face', label: 'Verifying Face' },
  { key: 'risk', label: 'Calculating Risk' },
];

// ---- Mock screening result ----------------------------------------------
// This simulates what a real verification backend would return after
// processing a document. It intentionally includes ONE low-confidence
// OCR field and ONE flagged tampering region so the UI's warning states
// are visible in the demo.
export function generateMockResult() {
  return {
    ocr: {
      name: { value: 'RAVI KUMAR SHARMA', confidence: 96 },
      idNumber: { value: 'DL-14 20230081234', confidence: 93 },
      dateOfBirth: { value: '14-08-1998', confidence: 62 }, // low confidence -> warning
      nationality: { value: 'INDIAN', confidence: 91 },
      expiryDate: { value: '13-08-2033', confidence: 95 },
    },

    validation: [
      {
        field: 'Expiry Date',
        status: 'pass',
        explanation: 'Document expiry date is valid and has not lapsed.',
      },
      {
        field: 'ID Format',
        status: 'pass',
        explanation: 'ID number matches the expected format for this document type.',
      },
      {
        field: 'Date of Birth',
        status: 'warning',
        explanation: 'OCR confidence for this field is below 70%. Manual review recommended.',
      },
      {
        field: 'Nationality',
        status: 'pass',
        explanation: 'Nationality field is present and consistent with document type.',
      },
    ],

    tampering: {
      level: 'Medium',
      score: 46, // out of 100, higher = more suspicious
      explanation:
        'A localized inconsistency was detected around the date-of-birth field, ' +
        'possibly caused by re-printing, pasting, or digital editing. This does not ' +
        'confirm forgery but warrants human review.',
      flagged: true,
      // Flagged region expressed as a percentage box over the document preview
      // so it scales responsively regardless of image size.
      flaggedRegion: { top: '38%', left: '10%', width: '46%', height: '14%' },
    },

    faceVerification: {
      similarity: 91,
      threshold: 75,
      match: true,
    },

    risk: {
      score: 46,
      level: 'MEDIUM',
      reasons: [
        { text: 'Expiry date is valid', tone: 'pass' },
        { text: 'ID format is valid', tone: 'pass' },
        { text: 'Possible tampering detected near date of birth', tone: 'warning' },
        { text: 'Date of birth OCR confidence is low (62%)', tone: 'warning' },
        { text: 'Face match: 91% (above threshold)', tone: 'pass' },
      ],
    },
  };
}