import React from 'react';
import {
	AbsoluteFill,
	interpolate,
	Sequence,
	spring,
	useCurrentFrame,
	useVideoConfig,
} from 'remotion';
import {loadFont as loadCormorant} from '@remotion/google-fonts/CormorantGaramond';
import {loadFont as loadInter} from '@remotion/google-fonts/Inter';


const {fontFamily: cormorant} = loadCormorant();
const {fontFamily: inter} = loadInter();

// ─── colour tokens ────────────────────────────────────────────────────────────
const INK = '#0a0f0d';
const SAGE = '#2d5a4b';
const GOLD = '#c8a96e';
const CARD_BG = '#111a16';

// ─── Scene 1: Brand intro ─────────────────────────────────────────────────────
const Scene1: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	// Cross SVG draws in over first 40 frames
	const crossProgress = interpolate(frame, [0, 40], [0, 1], {
		extrapolateRight: 'clamp',
	});
	const CROSS_LENGTH = 200; // total dash array length
	const strokeDashoffset = CROSS_LENGTH * (1 - crossProgress);

	// Letters spring in staggered
	const letters = ['V', 'I', 'T', 'A', 'R', 'A'];

	return (
		<AbsoluteFill
			style={{
				backgroundColor: INK,
				alignItems: 'center',
				justifyContent: 'center',
				flexDirection: 'column',
				gap: 48,
			}}
		>
			{/* Pharmacy cross SVG */}
			<svg width="120" height="120" viewBox="0 0 120 120">
				{/* vertical bar */}
				<line
					x1="60"
					y1="10"
					x2="60"
					y2="110"
					stroke={GOLD}
					strokeWidth="18"
					strokeLinecap="round"
					strokeDasharray={CROSS_LENGTH}
					strokeDashoffset={strokeDashoffset}
				/>
				{/* horizontal bar */}
				<line
					x1="10"
					y1="60"
					x2="110"
					y2="60"
					stroke={GOLD}
					strokeWidth="18"
					strokeLinecap="round"
					strokeDasharray={CROSS_LENGTH}
					strokeDashoffset={strokeDashoffset}
				/>
			</svg>

			{/* Brand name letter-by-letter spring */}
			<div style={{display: 'flex', gap: 6}}>
				{letters.map((letter, i) => {
					const delay = i * 4;
					const scale = spring({
						fps,
						frame: Math.max(0, frame - delay - 15),
						config: {damping: 10, stiffness: 120},
					});
					const opacity = interpolate(frame, [delay + 15, delay + 25], [0, 1], {
						extrapolateLeft: 'clamp',
						extrapolateRight: 'clamp',
					});
					return (
						<span
							key={i}
							style={{
								fontFamily: cormorant,
								fontSize: 112,
								fontWeight: 700,
								color: GOLD,
								letterSpacing: 8,
								opacity,
								transform: `scale(${scale})`,
								display: 'inline-block',
								lineHeight: 1,
							}}
						>
							{letter}
						</span>
					);
				})}
			</div>

			{/* Tagline */}
			<p
				style={{
					fontFamily: inter,
					fontSize: 22,
					color: 'rgba(200, 169, 110, 0.7)',
					letterSpacing: 6,
					textTransform: 'uppercase',
					opacity: interpolate(frame, [45, 58], [0, 1], {
						extrapolateLeft: 'clamp',
						extrapolateRight: 'clamp',
					}),
				}}
			>
				Premium Pharmacy Care
			</p>
		</AbsoluteFill>
	);
};

// ─── Scene 2: Split screen ────────────────────────────────────────────────────
const Scene2: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	const slideX = spring({fps, frame, config: {damping: 18, stiffness: 80}});
	const leftWidth = interpolate(slideX, [0, 1], [0, 540]);

	const textOpacity = interpolate(frame, [20, 38], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const textY = interpolate(frame, [20, 40], [30, 0], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	// Pill rotation
	const pillRotation = interpolate(frame, [10, 60], [0, 360], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	return (
		<AbsoluteFill style={{backgroundColor: INK, flexDirection: 'row'}}>
			{/* Left green panel */}
			<div
				style={{
					width: leftWidth,
					backgroundColor: SAGE,
					overflow: 'hidden',
					display: 'flex',
					alignItems: 'center',
					justifyContent: 'center',
					flexDirection: 'column',
					padding: 40,
				}}
			>
				<p
					style={{
						fontFamily: cormorant,
						fontSize: 46,
						fontStyle: 'italic',
						color: '#f0ead6',
						textAlign: 'center',
						lineHeight: 1.3,
						opacity: textOpacity,
						transform: `translateY(${textY}px)`,
						maxWidth: 420,
					}}
				>
					Prescriptions
					<br />
					Ready in Hours
				</p>
				<div
					style={{
						width: 60,
						height: 3,
						backgroundColor: GOLD,
						marginTop: 24,
						opacity: textOpacity,
					}}
				/>
			</div>

			{/* Right dark panel with pill */}
			<div
				style={{
					flex: 1,
					display: 'flex',
					alignItems: 'center',
					justifyContent: 'center',
					backgroundColor: '#0d1510',
				}}
			>
				{/* Animated pill icon */}
				<svg
					width="180"
					height="180"
					viewBox="0 0 180 180"
					style={{transform: `rotate(${pillRotation}deg)`}}
				>
					{/* Pill body */}
					<rect
						x="30"
						y="65"
						width="120"
						height="50"
						rx="25"
						fill="none"
						stroke={GOLD}
						strokeWidth="4"
					/>
					{/* Dividing line */}
					<line
						x1="90"
						y1="65"
						x2="90"
						y2="115"
						stroke={GOLD}
						strokeWidth="3"
					/>
					{/* Left half fill */}
					<path d="M30 90 Q30 65 55 65 H90 V115 H55 Q30 115 30 90Z" fill={SAGE} opacity="0.8" />
					{/* Right half fill */}
					<path d="M90 65 H125 Q150 65 150 90 Q150 115 125 115 H90Z" fill={GOLD} opacity="0.8" />
					{/* Center dot */}
					<circle cx="90" cy="90" r="6" fill="#fff" opacity="0.9" />
				</svg>
			</div>
		</AbsoluteFill>
	);
};

// ─── Scene 3: Service cards ───────────────────────────────────────────────────
const services = ['Compounding', 'Med Sync', 'Vaccines'];
const serviceIcons = ['⚗', '🔄', '💉'];

const ServiceCard: React.FC<{label: string; icon: string; delay: number}> = ({
	label,
	icon,
	delay,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	const ySpring = spring({
		fps,
		frame: Math.max(0, frame - delay),
		config: {damping: 14, stiffness: 100},
	});
	const opacity = interpolate(frame, [delay, delay + 12], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const translateY = interpolate(ySpring, [0, 1], [80, 0]);

	return (
		<div
			style={{
				backgroundColor: CARD_BG,
				border: `1.5px solid ${GOLD}`,
				borderRadius: 16,
				padding: '48px 36px',
				display: 'flex',
				flexDirection: 'column',
				alignItems: 'center',
				gap: 20,
				opacity,
				transform: `translateY(${translateY}px)`,
				flex: 1,
				minWidth: 0,
			}}
		>
			<span style={{fontSize: 52}}>{icon}</span>
			<span
				style={{
					fontFamily: inter,
					fontSize: 26,
					fontWeight: 600,
					color: GOLD,
					letterSpacing: 1,
					textAlign: 'center',
				}}
			>
				{label}
			</span>
			<div
				style={{
					width: 40,
					height: 2,
					backgroundColor: SAGE,
					borderRadius: 1,
				}}
			/>
		</div>
	);
};

const Scene3: React.FC = () => {
	return (
		<AbsoluteFill
			style={{
				backgroundColor: INK,
				alignItems: 'center',
				justifyContent: 'center',
				flexDirection: 'column',
				padding: '80px 60px',
				gap: 40,
			}}
		>
			<p
				style={{
					fontFamily: cormorant,
					fontSize: 48,
					color: '#e8e0d0',
					letterSpacing: 3,
					textAlign: 'center',
					fontStyle: 'italic',
				}}
			>
				Our Services
			</p>
			<div
				style={{
					display: 'flex',
					gap: 28,
					width: '100%',
					alignItems: 'stretch',
				}}
			>
				{services.map((svc, i) => (
					<ServiceCard key={svc} label={svc} icon={serviceIcons[i]} delay={i * 8} />
				))}
			</div>
		</AbsoluteFill>
	);
};

// ─── Scene 4: Testimonial ─────────────────────────────────────────────────────
const QUOTE_WORDS = [
	'"The',
	'pharmacist',
	'called',
	'me',
	'back',
	'the',
	'same',
	'evening."',
];

const Scene4: React.FC = () => {
	const frame = useCurrentFrame();

	const authorOpacity = interpolate(frame, [55, 68], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	return (
		<AbsoluteFill
			style={{
				backgroundColor: '#08110d',
				alignItems: 'center',
				justifyContent: 'center',
				flexDirection: 'column',
				padding: '100px 80px',
				gap: 48,
			}}
		>
			{/* Decorative quote mark */}
			<span
				style={{
					fontFamily: cormorant,
					fontSize: 180,
					color: SAGE,
					lineHeight: 0.5,
					opacity: 0.3,
					alignSelf: 'flex-start',
					marginLeft: 20,
				}}
			>
				"
			</span>

			{/* Word-by-word reveal */}
			<div
				style={{
					display: 'flex',
					flexWrap: 'wrap',
					gap: '0 14px',
					justifyContent: 'center',
					marginTop: -60,
				}}
			>
				{QUOTE_WORDS.map((word, i) => {
					const wordStart = i * 7;
					const opacity = interpolate(frame, [wordStart, wordStart + 10], [0, 1], {
						extrapolateLeft: 'clamp',
						extrapolateRight: 'clamp',
					});
					const y = interpolate(frame, [wordStart, wordStart + 12], [16, 0], {
						extrapolateLeft: 'clamp',
						extrapolateRight: 'clamp',
					});
					return (
						<span
							key={i}
							style={{
								fontFamily: cormorant,
								fontStyle: 'italic',
								fontSize: 68,
								fontWeight: 500,
								color: '#f0ead6',
								opacity,
								transform: `translateY(${y}px)`,
								display: 'inline-block',
								lineHeight: 1.35,
							}}
						>
							{word}
						</span>
					);
				})}
			</div>

			{/* Attribution */}
			<div
				style={{
					opacity: authorOpacity,
					display: 'flex',
					flexDirection: 'column',
					alignItems: 'center',
					gap: 12,
				}}
			>
				<div style={{width: 80, height: 1.5, backgroundColor: GOLD}} />
				<p
					style={{
						fontFamily: inter,
						fontSize: 24,
						color: GOLD,
						letterSpacing: 4,
						textTransform: 'uppercase',
					}}
				>
					Margaret T.
				</p>
				<p
					style={{
						fontFamily: inter,
						fontSize: 18,
						color: 'rgba(200,169,110,0.6)',
						letterSpacing: 2,
					}}
				>
					Loyal Customer since 2019
				</p>
			</div>
		</AbsoluteFill>
	);
};

// ─── Scene 5: CTA ─────────────────────────────────────────────────────────────
const Scene5: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	// Logo spring in
	const logoSpring = spring({fps, frame, config: {damping: 14, stiffness: 90}});

	// "Transfer in 5 minutes" pulse
	const pulse = Math.sin((frame / 6) * Math.PI) * 0.06 + 1;

	// Phone number count-up: 1-800-VITARA
	// Animate digits appearing
	const phoneDigits = '1-800-VITARA';
	const visibleChars = Math.floor(
		interpolate(frame, [18, 42], [0, phoneDigits.length], {
			extrapolateLeft: 'clamp',
			extrapolateRight: 'clamp',
		})
	);

	// Gold button slide up
	const btnY = interpolate(frame, [35, 52], [60, 0], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const btnOpacity = interpolate(frame, [35, 52], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	// Subtext
	const subOpacity = interpolate(frame, [50, 62], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	return (
		<AbsoluteFill
			style={{
				backgroundColor: INK,
				alignItems: 'center',
				justifyContent: 'center',
				flexDirection: 'column',
				gap: 44,
				padding: '80px 60px',
			}}
		>
			{/* Logo lockup */}
			<div
				style={{
					display: 'flex',
					flexDirection: 'column',
					alignItems: 'center',
					gap: 20,
					transform: `scale(${logoSpring})`,
				}}
			>
				{/* Mini cross */}
				<svg width="56" height="56" viewBox="0 0 56 56">
					<line x1="28" y1="6" x2="28" y2="50" stroke={GOLD} strokeWidth="8" strokeLinecap="round" />
					<line x1="6" y1="28" x2="50" y2="28" stroke={GOLD} strokeWidth="8" strokeLinecap="round" />
				</svg>
				<span
					style={{
						fontFamily: cormorant,
						fontSize: 72,
						fontWeight: 700,
						color: GOLD,
						letterSpacing: 10,
					}}
				>
					VITARA
				</span>
				<span
					style={{
						fontFamily: inter,
						fontSize: 18,
						color: 'rgba(200,169,110,0.65)',
						letterSpacing: 5,
						textTransform: 'uppercase',
					}}
				>
					Pharmacy
				</span>
			</div>

			{/* Divider */}
			<div style={{width: '60%', height: 1, backgroundColor: `${GOLD}44`}} />

			{/* Pulsing CTA line */}
			<p
				style={{
					fontFamily: inter,
					fontSize: 34,
					fontWeight: 600,
					color: '#e8e0d0',
					letterSpacing: 1,
					textAlign: 'center',
					transform: `scale(${pulse})`,
				}}
			>
				Transfer in{' '}
				<span style={{color: GOLD}}>5 minutes</span>
			</p>

			{/* Phone count-up */}
			<p
				style={{
					fontFamily: cormorant,
					fontStyle: 'italic',
					fontSize: 48,
					color: SAGE,
					letterSpacing: 4,
				}}
			>
				{phoneDigits.slice(0, visibleChars)}
				<span style={{opacity: 0.2}}>{phoneDigits.slice(visibleChars)}</span>
			</p>

			{/* Gold CTA button */}
			<div
				style={{
					backgroundColor: GOLD,
					borderRadius: 60,
					paddingTop: 28,
					paddingBottom: 28,
					paddingLeft: 80,
					paddingRight: 80,
					transform: `translateY(${btnY}px)`,
					opacity: btnOpacity,
				}}
			>
				<span
					style={{
						fontFamily: inter,
						fontSize: 28,
						fontWeight: 700,
						color: INK,
						letterSpacing: 2,
						textTransform: 'uppercase',
					}}
				>
					Get Started Today
				</span>
			</div>

			{/* Fine print */}
			<p
				style={{
					fontFamily: inter,
					fontSize: 16,
					color: 'rgba(200,169,110,0.45)',
					letterSpacing: 2,
					textAlign: 'center',
					opacity: subOpacity,
				}}
			>
				vitarapharmacy.com · Free consultations
			</p>
		</AbsoluteFill>
	);
};

// ─── Main composition ─────────────────────────────────────────────────────────
export const VitaraAd: React.FC = () => {
	return (
		<AbsoluteFill style={{backgroundColor: INK}}>
			<Sequence from={0} durationInFrames={60}>
				<Scene1 />
			</Sequence>

			<Sequence from={60} durationInFrames={70}>
				<Scene2 />
			</Sequence>

			<Sequence from={130} durationInFrames={70}>
				<Scene3 />
			</Sequence>

			<Sequence from={200} durationInFrames={60}>
				<Scene4 />
			</Sequence>

			<Sequence from={260} durationInFrames={40}>
				<Scene5 />
			</Sequence>
		</AbsoluteFill>
	);
};
