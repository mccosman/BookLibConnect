import React from 'react';
import {Composition} from 'remotion';
import {VitaraAd} from './VitaraAd';

export const RemotionRoot: React.FC = () => {
	return (
		<>
			<Composition
				id="VitaraAd"
				component={VitaraAd}
				durationInFrames={300}
				fps={30}
				width={1080}
				height={1920}
			/>
		</>
	);
};
