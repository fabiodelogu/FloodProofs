      common /declaration/ dem ,ipun ,pdistance , &
          iarea , ichoice , idim, jdim, step, const,musk, fslope,mattmp
	  

	  integer*4	, pointer :: ichoice(:,:), musk(:,:)

	  integer*4	, pointer :: ipun(:,:), iarea(:,:),mattmp(:,:)

	  real		, pointer :: dem(:,:),pdistance(:,:), fslope(:,:)

	  integer*4   idim, jdim, step, const

	  real pmedia, sm

	 
